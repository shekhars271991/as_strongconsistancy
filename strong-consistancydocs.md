# Strong consistency

This page describes how to use strong consistency (SC) mode in Aerospike Database. Strong consistency is available only in Aerospike Database Enterprise Edition and Aerospike Cloud Managed Service.

::: tip
You can learn more about Available and Partition-tolerant (AP) mode and SC mode in [Consistency modes](https://aerospike.com/docs/database/learn/architecture/clustering/consistency-modes).
:::

## Guaranteed writes and partition availability

SC mode guarantees that all writes to a single record will be applied in a specific, sequential order, and writes will not be re-ordered or skipped; in other words data will not be lost. The following are exceptions to this guarantee:

-   A cluster node’s Aerospike process (`asd`) pauses for more than 27 seconds, or the clock skew between cluster nodes is greater than 27 seconds.
    
    ::: note
    The clock skew threshold of 27 seconds is based on the default [heartbeat `interval`](https://aerospike.com/docs/database/reference/config#network__interval) of 150 ms and the default [heartbeat `timeout`](https://aerospike.com/docs/database/reference/config#network__timeout) of 10. If those defaults are changed, the clock skew threshold is increased or decreased accordingly.
    :::
    
    In the case of clock skew, Aerospike’s gossip cluster protocol continually monitors the amount of skew. It sends an alert if the skew of any node becomes large, and disables writes to the cluster at 20 seconds for default settings, before data loss would occur at 27 seconds default skew.
    
-   A [`replication-factor`](https://aerospike.com/docs/database/reference/config#namespace__replication-factor) (RF) number of servers shutting down uncleanly and [`commit-to-device`](https://aerospike.com/docs/database/reference/config#namespace__commit-to-device) is not enabled.
    
    ::: note
    A clean shutdown starts with a SIGTERM signal and ends with the Aerospike process (`asd`) stopping after logging `finished clean shutdown - exiting`. This ensures that `asd` flushed data to disk and properly signalled other servers in the cluster. Server crashes and other signals, for example, SIGKILL, cause unclean shutdowns.
    :::
    
-   Data devices on RF number of cluster nodes in the roster were wiped while `asd` was shut down.
    

### Unavailable partitions

In each failure scenario affecting a namespace running in SC mode, Aerospike attempts to provide the best availability and minimize potential issues. If nodes that are expected in the roster are missing from the cluster, their data partitions might become unavailable. Read-only access to records in an unavailable or dead partition is allowed under the most relaxed SC read mode `ALLOW_UNAVAILABLE` allowing stale but not dirty reads, and for reloading of recent changes.

The [Consistency](https://aerospike.com/docs/database/learn/architecture/clustering/consistency-modes#roster-of-nodes) architecture guide describes the concepts of the roster, full partitions and subsets, and the simple rules governing whether a partition becomes unavailable when an RF number of rostered nodes are missing from the cluster. If less nodes go down than the RF, all partitions remain available.

The initial step to deal with unavailable partitions is to restore the missing nodes by fixing the hardware or network issues causing them to be out of the cluster.

### Dead partitions

When a node goes down due to an unclean shutdown, its data will not be immediately trusted when it starts up and rejoins the cluster. The node is marked with an “evade flag” (“e flag”), and is not counted in the super-majority math. At this point unavailable partitions might transition to dead partitions to designate that they have potentially suffered lost writes.

Operators should inspect the scenario that lead to the dead partitions, consider if writes were actually lost, and decide whether to manually revive them. There are several mitigations that can be used to significantly reduce the chances of actual data loss, and an auto-revive configuration allows operators to direct Aerospike to skip waiting for manual intervention before reviving dead partitions in certain situations. See below for more details.

Shutting down a node before it has completed a fast restart also causes an unclean shutdown. It does not lead to data loss but may lead to dead partitions. This scenario can be safely mitigated with a revive.

### Manually reviving dead partitions

If RF cluster nodes went down due to an unclean shutdown there is a risk of lost writes if all nodes went down within a time interval less than [`flush-max-ms`](https://aerospike.com/docs/database/reference/config#namespace__flush-max-ms). If the operator knows this is not the case, the dead partitions may be safely revived.

If data devices were wiped on RF number of nodes, the operator must recover this data from an external source, if available. Otherwise, reviving the dead partitions in this scenario results in lost data. Consider disabling the applications, reviving the damaged namespace, restoring from the external trusted source, and then enabling applications.

### Auto revive

Aerospike Database 7.1.0 introduced the [`auto-revive`](https://aerospike.com/docs/database/reference/config#namespace__auto-revive) configuration, which revives dead partitions caused by the scenario where RF roster nodes went down due to unclean shutdowns. Auto revive is selective; it will not revive partitions in the scenario of RF nodes having their storage devices wiped. That case must be manually mitigated, as described above.

### Mitigating the effects of unclean shutdowns

The effect of an unclean shutdown can be completely avoided by setting the `commit-to-device` namespace option. With this option, simultaneous crashes do not cause data loss, and never generate dead partitions. However, enabling `commit-to-device` generates a flush on every write, and comes with performance penalties except for low write throughput use cases.

When using the persistent memory (PMem) storage for the namespace `commit-to-device` suffers no noticeable performance penalty. Similarly, if the namespace data storage is shared memory (RAM) without storage-backed persistence, as of Database 7.0.0 `commit-to-device` has no performance penalty at all.

### Reducing the chance of lost data

When `commit-to-device` isn’t used due to performance considerations, a rack-aware deployment will reduce the chance of RF number of nodes going down due to unclean shutdowns within one `flush-max-ms` interval. In a cloud deployment each rack lives in a different Availability Zone (AZ), which are independent datacenters and have separate hardware resources such as power or networking. An operator may choose to use `auto-revive` in a multi-AZ deployment based on the reduced likelihood of this failure scenario.

## Configuring for strong consistency

SC mode is enabled on an entire namespace. For information about enabling SC mode on a namespace, see [Configure strong consistency](https://aerospike.com/docs/database/manage/namespace/consistency).

## Managing strong consistency

[Cluster consistency](https://aerospike.com/docs/database/manage/cluster/consistency) describes adding and removing nodes, starting and stopping servers cleanly, how to validate partition availability, and how to revive dead partitions. It also describes the `auto-revive` feature added in Database 7.1.0.

## Using strong consistency

The following sections discuss new API functionality related to SC. In general, SC mode is transparent to the developer. Primarily, you simply know that data is safe.

However, there are some new capabilities, managed through the client [`Policy`](https://aerospike.com/docs/database/learn/policies) object, as well as differences in error code meanings.

### Linearizable reads

A new field exists on the `Policy` object. In order to attain linearizable reads, you must set the `linearizableRead` field to `true`. If you set this field to a read on a non-SC configured namespace, the read will fail. If you do not set this field on an SC namespace, you will get Session Consistency.

The `Policy` object can be set in the initial AerospikeClient constructor call. All subsequent calls using the constructed AerospikeClient object will, by default, use that value. Otherwise, you should use this constructed Policy object on individual operations to denote whether to execute a fully linearized read, or a Session Consistency read.

Several Policy objects - `BatchPolicy`, `WritePolicy`, `QueryPolicy`, and `ScanPolicy` - inherit from the `Policy` object. Of these, the new `linearizableRead` field only makes sense for the default object and the inherited BatchPolicy object, where it is applied for all elements in the batch operation.

### InDoubt errors

A new field on all error returns called `InDoubt` has been added. This is to denote the difference where a write has _certainly_ not been applied, or _may_ have been applied.

In most database APIs, such as the SQL standard, failures like TIMEOUT are “known” to be uncertain, but there is no specific flag to denote which errors are uncertain. Common practice is to read the database to determine if a writes has been applied.

For example, if the client driver timed out before contacting a server, the client driver may be certain that the transaction was not applied; if the client has attached to a server and sent the data but receives no response over TCP, the client is unsure whether the write has been applied. The Aerospike API improvement allows the client to denote which failures have _certainly_ not been applied.

We believe this flag can be useful for the advanced programmer and reduce cases where an error requires reading from the database under high stress situations.

### Data unreachable errors

In SC, there will be periods where data is unavailable because of network partition or other outage. There are several errors the client could present if data is, or becomes, unavailable.

These errors already exist in Aerospike, but have important distinctions when running with SC. Here are the list of errors for some of the main client libraries:

-   [Java client](https://aerospike.com/apidocs/java/com/aerospike/client/ResultCode.html)
    
-   [C# client](https://aerospike.com/apidocs/csharp/api/Aerospike.Client.ResultCode.html)
    
-   [C client](https://aerospike.com/apidocs/c/dc/d42/as__status_8h.html)
    
-   [Go client](https://pkg.go.dev/github.com/aerospike/aerospike-client-go/v8#AerospikeError)
    
-   [Node.js](https://aerospike.com/apidocs/nodejs/modules/status.html)
    

Four different errors can be seen when a cluster has partitioned, or has multiple hardware failures resulting in data unavailability (using here the Java Client error codes): `PARTITION_UNAVAILABLE`, `INVALID_NODE_ERROR`, `TIMEOUT` and `CONNECTION_ERROR`.

::: note
Other clients may have different error codes for those conditions. Refer to the Client Library specific error code tables for details.
:::

The error `PARTITION_UNAVAILABLE` is returned from the server when that server determines that its cluster does not have the correct data. In specific, the client can connect to a cluster, and has received a partition table that includes this partition data initially. In this case, the client will send a request to the most recent server it has heard from. If that server is part of a cluster that no longer has data availability, the `PARTITION_UNAVAILABLE` error will be returned.

The error `INVALID_NODE_ERROR` is generated by the client in cases where the client does not have a node to send a request to. This happens initially when the specified “seed node” addresses are incorrect, when the client can’t connect to the particular node(s) in the list of seeds and thus never receives a full partition map, and also when the partition map received from the server does not contain the partition in question.

`INVALID_NODE_ERROR` will also occur if the roster has been mis-configured, or if the server has [`dead_partitions`](https://aerospike.com/docs/database/reference/metrics#namespace__dead_partitions) or [`unavailable_partitions`](https://aerospike.com/docs/database/reference/metrics#namespace__unavailable_partitions) and needs maintenance or re-clustering. If you get this error, validate that data in the cluster is available using the steps above.

Two other errors, `TIMEOUT` and `CONNECTION_ERROR`, will be returned in cases where a network partition has happened or is happening. The client must have a partition map and thus a node to send the request to, but can’t connect to that node, or has connected but subsequently the failure occurs. The `CONNECTION_ERROR` may persist as long as the network partition, and only goes away when the partition has been healed or operator intervention has changed the cluster rosters.

## Strong consistency guarantees

SC guarantees a session (a client instance in our SDKs) will observe writes to a record in the order that they are applied. This means that if the client reads the record and then reads it again, this read is guaranteed to be a committed version in the records lineage from the point of the prior read onward. Linearizability extends this guarantee to across all concurrent sessions, meaning that if a session reads the records after another session, then the record is guaranteed to be the same or newer than the one from the other session.

In particular, writes that are acknowledged as committed have been applied, and exist in the transaction timeline in contrast to other writes to the same record. This guarantee applies even in the face of network failures and outages, and partitions. Writes which are designated as “timeouts” or “InDoubt” from the client API may or may not be applied, but if they have been applied they will only be observed as such.

Aerospike’s strong consistency guarantee is per-record, and involves no multi-record transaction semantics. Each record’s write or update will be atomic and isolated, and ordering is guaranteed using a hybrid clock.

Aerospike provides both full linearizable mode, which provides a single linear view among all clients that can observe data, as well as a more practical session consistency mode, which guarantees an individual process sees the sequential set of updates. These two read policies can be chosen on a read-by-read basis, thus allowing the few transactions that require a higher guarantee to pay the extra synchronization price, and are detailed below.

In the case of a _timeout_ return value, which could be generated due to network congestion and is external to any Aerospike issue, the write is atomic from the application’s point of view. This means that the write is guaranteed to be written completely or not written at all.

This does not preclude situations where the exact state of the record may be unknown for a while due to network connectivity issues. An example is a “split-brain” that causes a single cluster to be partitioned into two or more sub-clusters that are isolated from each other on the network. For certain writes that are in progress when a split-brain is forming, the system can return an _in-doubt_ status for a while until network connectivity is restored at a later time, thus curing the split-brain situation. The in-doubt status is cleared once the split-brain is cured and the application can determine whether the write was completed or not.

In case of a failure to replicate a write transaction across all replicas, the record is left in the _un-replicated_ state, forcing a _re-replication_ transaction prior to any subsequent read or write transaction on the record.

::: note
SC is configured on a per-namespace basis. Switching a namespace from one mode to another is impractical. We recommend that you create a new namespace and migrate your data.
:::

### Linearizability

In concurrent programming, an operation or set of operations is atomic, linearizable, indivisible or uninterruptible if it appears to the rest of the system to occur instantaneously - or is made available for reads instantaneously.

All accesses are seen by all parallel processes in the same order, sequentially. This guarantee is enforced by the Aerospike effective master for the record, and results in an in-transaction “health check” to determine the state of the others servers.

If a write is applied and observed to be applied by a client, no prior version of the record will be observed. With this client mode enabled, “global consistency” - referring to all clients attaching to the cluster - will see a single view of record state at a given time.

This mode requires extra synchronization on every read, thus incurs a performance penalty. Those synchronization packets do not look up or read individual records, but instead simply validate the existence and health of individual partition.

### Session consistency

This mode, called in other databases by the names “Monotonic reads, monotonic writes, read-your-writes, write-follows-reads”, is the most practical of strong consistency modes.

Unlike the linearizable model, session consistency is scoped to a client session - which in this case is an Aerospike cluster object on an individual client system, unless shared memory shares cluster state between processes.

Session consistency is ideal for all scenarios where a device or user session is involved since it guarantees monotonic reads, monotonic writes, and read your own writes (RYW) guarantees.

Session consistency provides predictable consistency for a session, and maximum read throughput while offering the lowest latency writes and reads.

## Performance considerations

SC mode is similar to Availability mode in performance when used with the following settings:

1.  Replication factor two,
2.  Session Consistency.

When the replication factor is more than 2, a write causes an extra “replication advise” packet to acting replicas. While the master does not wait for a response, the extra network packets will create load on the system.

When the linearizability read concern is enabled, during a read the master must send a request to every acting replica. These “regime check” packets - which do not do full reads - cause extra latency and packet load, and decrease performance.

## Availability considerations

Although Aerospike allows operation with two copies of the data, availability in a failure case requires a replica during a master promotion, which then requires during the course of a failure three copies, the copy that failed, the new master, and the prospective replica. Without this third potential copy, a partition may remain unavailable. For this reason, a two node cluster - with two copies of the data - is not available in a split.

## Exceptions to consistency guarantees

This section describes some operational circumstances which could cause issues with consistency or durability.

### Clock discontinuity

A clock discontinuity of more than approximately 27 seconds may result in lost writes. In this case, data is written to storage with a time value outside the 27-second clock resolution. A subsequent data merge may pick this uncommitted write over other successfully completing versions of the record, due to the precision of the stored clock values.

In the case where the discontinuity is less than 27 seconds, the resolution of the internal hybrid clock will choose the correct record.

Organic clock skew is not an issue, the cluster’s heartbeat mechanism detects the drift at a skew of 15 seconds by default, and logs warnings. If the skew becomes extreme, 20 seconds by default, the node rejects writes, returning the “forbidden” error code, thus preventing consistency violations.

Clock discontinuities of this type tend to occur due to four specific reasons:

1.  Administrator Error, where an operator executes setting the clock far into the future or far into the past
2.  Malfunctioning time synchronization components
3.  Hibernation of virtual machines
4.  Linux process pause or Docker container pause

Be certain to avoid these issues.

### Clock discontinuity due to virtual machine live migrations

Virtual machines and virtualized environments, can result in safe strong consistency deployments.

However, two specific configuration issues are hazardous.

**Live migrations**, which is the process of moving a virtual machine from one physical chassis to another transparently, causes certain hazards. Clocks move with discontinuities, and network buffers can remain in lower level buffers and be applied later.

If live migrations can be certainly limited to less than 27 seconds, strong consistency can be maintained. However, the better operational process is to safely stop Aerospike, move the virtual machine, then restart Aerospike.

The second case involves process pauses, which are also used in container environments. These create similar hazards, and should not be executed. There are few operational reasons to use these features,

### UDFs

The UDF system will function, but, currently, UDF reads will not be linearized, and UDF writes that fail in certain ways may result in inconsistencies.

### Non-durable deletes, expiration, and data eviction

Non-durable deletes, including data expiration and eviction, are not strongly consistent. These removals from the database do not generate persistent “tombstones” so they may violate strong consistency guarantees. In these cases you may see data return. For this reason, we generally require disabling eviction and expiration in SC configurations, however, as there are valid use cases, we allow manual override.

However, there are cases where expiration and non-durable deletes may be required even for SC namespaces, and may be known to be safe to the architects, programmers, and operations staff.

These are generally cases where a few objects are being modified, and “old” objects are being expired and deleted. No writes are possible to objects which may be subject to expiration or deletion.

For example, writes may occur to an object - which represents a financial transaction - for a few seconds, then the object may exist in the database for several days without writes. This object may safely be expired, as the period of time between the writes and the expiration is very large.

If you are certain that your use case is suitable, you may enable non-durable deletes. Use the following configuration setting in your `/etc/aerospike/aerospike.conf` adding a namespace option:

```plaintext
strong-consistency-allow-expunge true
```

Durable deletes, which do generate tombstones, fully support strong consistency.

## Client retransmit

If you enable Aerospike client write retransmission, you may find that certain test suites will claim consistency violation. This is because an initial write results in a timeout, and is thus retransmitted, and potentially applied multiple times.

Several hazards are present.

First, the write may be applied multiple times. This write may then “surround” other writes, causing consistency violations. This can be avoided using the “read-modify-write” pattern and specifying a generation, as well as disabling retransmission.

Second, incorrect error codes may be generated. For example, a write may be correctly applied but a transient network fault might cause retransmission. On the second write, the disk may be full, generating a specific and not “InDoubt” error - even though the transaction was applied. This class of error can’t be resolved by using the “read-modify-write” pattern.

We strongly recommend disabling the client timeout functionality, and retransmitting as desired in the application. While this may seem like extra work, the benefits of correct error codes while debugging is invaluable.

## Secondary index requests

If a query is executed, both stale reads and dirty reads may be returned. In the interest of performance, Aerospike currently returns data that is “In Doubt” on a master and has not been fully committed.

This violation only exists for queries, and will be rectified in subsequent releases.

## Durability exceptions

### Storage hardware failure

Some durability exceptions are detected, marking the partition as a `dead_partition` in administrative interfaces.

This happens when all nodes within the entire roster are available and connected, yet some partition data is not available. To allow a partition to accept reads and writes again, execute a “revive” command to override the error, or bring a server online with the missing data. Revived nodes restore availability only when all nodes are trusted.

These cases occur when SC is used with a data in memory configuration with no backing store, or when backing storage is either erased or lost.

Database 7.1.0 introduced the [`auto-revive`](https://aerospike.com/docs/database/reference/config#namespace__auto-revive) feature which selectively revives some partitions on startup.

### Incorrect roster management

Reducing the roster by replication-factor or more nodes at a time may result in loss of record data. The procedure for safe addition and removal from a cluster must be followed. Follow the operational procedures regarding roster management closely.

### Partial storage erasure

In the case where some number of sectors or portions of a drive have been erased by an operator, Aerospike is unable to note the failure. Partial data erasure, such as malicious user actions or drive failure on replication-factor or more nodes, may erase records and escape detection.

### Simultaneous server restarts

By default, Aerospike writes data initially to a buffer, and considers the data written when all the required server nodes have acknowledged receiving the data and placing it in the persistent queue.

Aerospike attempts to remove all other write queues from the system. The recommended Aerospike hardware configuration uses a RAW device mode which disables all operating system page caches and most device caches. We recommend disabling any hardware device write caches, which must be done in a device-specific fashion.

Aerospike will immediately begin the process of replicating data in case of a server failure. If replication occurs quickly, no writes will be lost.

In order to protect against data loss in the write queue during multiple rapid failures, enable `commit-to-device` noted elsewhere. The default algorithms cause the data lost to be limited and provide the highest levels of performance, but this feature can be enabled on an individual storage-based namespace if the higher level of guarantee is required.

In the case where a filesystem or device with a write buffer is used as storage, `commit-to-device` may not prevent these kind of buffer based data losses.

## Upgrading from AP to SC namespaces

In general, changing a namespace from AP to SC is not supported. There are cases where consistency violations may occur during the change. We recommend that you create a new namespace, then back up and restore use (the [forklift](https://www.architecting.it/blog/what-is-a-forklift-upgrade/#:~:text=The%20term%20%E2%80%9Cforklift%20upgrade%E2%80%9D%20refers,like%20snapshots%20and%20remote%20replication.) upgrade procedure).