# Configure strong consistency

This page describes how to configure a namespace with [strong consistency](https://aerospike.com/docs/database/manage/namespace/consistency) (SC). Aerospike’s [consistency modes](https://aerospike.com/docs/database/learn/architecture/clustering/consistency-modes) are explained in the architecture section.

## Quickstart

Following are two methods for an initial set up of an SC namespace.

### Manually configuring an SC-enabled namespace

The following is the required minimum configuration to get started quickly with an SC namespace:

-   [Acquire an SC-enabled feature-key file](#acquire-an-sc-enabled-feature-key-file).
-   Set the [`strong-consistency`](https://aerospike.com/docs/database/reference/config#namespace__strong-consistency) namespace configuration parameter to `true`.
-   SC requires at least as many nodes in the cluster as the namespace replication factor. In a single-node cluster deployment make sure to set the namespace [`replication-factor`](https://aerospike.com/docs/database/reference/config#namespace__replication-factor) to 1.
-   [Configure the initial roster](#configure-the-initial-roster).

### Using AeroLab to deploy an SC-enabled cluster

You can use the [AeroLab](https://github.com/aerospike/aerolab/blob/master/README.md) tool to automatically deploy and configure Aerospike development clusters locally in Docker, or remotely on AWS or Google Cloud. To try out the new [transactions](https://aerospike.com/docs/database/learn/transactions) feature of Aerospike Database 8, do the following to set up an SC-enabled cluster in a container:

Terminal window

```bash
aerolab config backend -t docker

aerolab cluster create -f features.conf

aerolab conf sc
```

The `conf sc` command handles all the SC configuration steps.

## Acquire an SC-enabled feature-key file

A [feature-key file](https://aerospike.com/docs/database/manage/planning/feature-key) is required for starting Aerospike Database Enterprise Edition (EE) cluster nodes. The `asdb-strong-consistency` feature-key is required to enable SC mode.

Aerospike customers can access their feature-key file through the support portal. The container image of Aerospike EE is bundled with a feature-key file which provides a perpetual single-node evaluation. The [_Try Now_](https://aerospike.com/try-now/) section on the _Get started with Aerospike Database_ page provides a feature-key file for a 60-day multi-node EE evaluation. Both include the `asdb-strong-consistency` feature-key.

## Assign node IDs (optional)

Aerospike [`node-id`](https://aerospike.com/docs/database/reference/config#service__node-id) is an 8 byte number which is derived using the server’s MAC address and the fabric port by default. The 6 least significant bytes are copied from the MAC address, and the 2 most significant bytes are copied from the fabric port.

::: note
Consider manually assigning node IDs for your SC-enabled cluster. Hardware-generated node IDs, while convenient for availability mode’s automatic algorithms, can become cumbersome when managing SC.
:::

-   For more readable node IDs, you can configure a specific 1 to 16 character hexadecimal `node-id` for each node. For example, “`01`” and “`B2`” and “`beef`” are valid, but “`fred`” is not.
    -   This feature works with cloud providers such as Amazon AWS. Specifying a `node-id` to match a particular EBS volume allows for a node to be removed and a new instance created without having to change the `node-id` when you bring up Aerospike with the new instance.
-   The cluster does not allow nodes with duplicate `node-id`s to join the cluster. The refusal is noted in the log file.

To convert a cluster from automatic to assigned node IDs, you will change the configuration file for a server and restart. For an SC namespace, you will have to change the roster. To prevent data unavailability, if you are changing multiple servers, update a single server, restart it, modify and commit the new roster, then repeat for the next server. You do not have to wait until data migration finishes, but you must validate and apply the new roster.

To configure the node ID, edit your configuration file and add `node-id <HEX NODE ID>` to the service context.

::: caution
The configuration file options [`node-id`](https://aerospike.com/docs/database/reference/config#service__node-id) and [`node-id-interface`](https://aerospike.com/docs/database/reference/config#service__node-id-interface) are mutually exclusive.
:::

Terminal window

```bash
service {

    user root

    group root

    nsup-period 16

    proto-fd-max 15000

    node-id a1

}
```

When the server starts, validate that the `node-id` is as expected, then change the roster of any SC namespace intending to include this server.

## Configure the initial roster

The roster is the list of nodes which are expected to be in the cluster, for this particular SC namespace. This list is stored persistently in a distributed table within each Aerospike server, similar to how index configuration is stored. In order to change and manipulate this roster, use the following Aerospike real-time tools. The tools referenced here are part of the Aerospike tools package, which should be installed.

Rosters are specified using node IDs. You can specify the node ID of each server, or use the automatically generated node ID. For further information about specifying node IDs, see that section.

The general process of managing a roster is to first bring together the cluster of nodes, then list the node IDs within the cluster that have the namespace defined, and finally add the node’s IDs to the roster. To commit the changes, execute a recluster command.

### Configure roster with asadm

Do this with the following commands:

Terminal window

```bash
Admin> enable;

Admin+> manage roster stage observed ns test

Pending roster now contains observed nodes.

Run "manage recluster" for your changes to take affect.

Admin+> manage recluster

Admin+> pager on

Admin+> show roster

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Roster (2021-10-22 20:14:01 UTC)~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

                    Node|         Node ID|Namespace|                                 Current Roster|                                 Pending Roster|                                 Observed Nodes

node2.aerospike.com:3000|BB9070016AE4202 |test     |BB9070016AE4202,BB9060016AE4202,BB9050016AE4202|BB9070016AE4202,BB9060016AE4202,BB9050016AE4202|BB9070016AE4202,BB9060016AE4202,BB9050016AE4202

node4.aerospike.com:3000|BB9060016AE4202 |test     |BB9070016AE4202,BB9060016AE4202,BB9050016AE4202|BB9070016AE4202,BB9060016AE4202,BB9050016AE4202|BB9070016AE4202,BB9060016AE4202,BB9050016AE4202

node6.aerospike.com:3000|*BB9050016AE4202|test     |BB9070016AE4202,BB9060016AE4202,BB9050016AE4202|BB9070016AE4202,BB9060016AE4202,BB9050016AE4202|BB9070016AE4202,BB9060016AE4202,BB9050016AE4202

Number of rows: 3
```

### Configure roster with asinfo

Optionally, you can use the equivalent [asinfo](https://aerospike.com/docs/database/reference/info#roster) commands:

1.  Get a list of nodes with this namespace definition.
    
    Terminal window
    
    ```bash
    asinfo -v 'roster:namespace=[ns-name]'
    ```
    
    The `observed_nodes` are the nodes which are in the cluster and have the namespace defined.
    
2.  Copy the `observed_nodes list`.
    
    Terminal window
    
    ```bash
    Admin+> asinfo -v "roster:namespace=test"
    
    node6.aerospike.com:3000 (192.168.10.6) returned:
    
    roster=null:pending_roster=null:observed_nodes=BB9070016AE4202,BB9060016AE4202,BB9050016AE4202
    
    node4.aerospike.com:3000 (192.168.10.4) returned:
    
    roster=null:pending_roster=null:observed_nodes=BB9070016AE4202,BB9060016AE4202,BB9050016AE4202
    
    node2.aerospike.com:3000 (192.168.10.2) returned:
    
    roster=null:pending_roster=null:observed_nodes=BB9070016AE4202,BB9060016AE4202,BB9050016AE4202
    ```
    
3.  Set the roster to the `observed_nodes`.
    
    Terminal window
    
    ```bash
    roster-set:namespace=[ns-name];nodes=[observed nodes list]
    ```
    
    ::: note
    It is safe to issue this command multiple times, once for each observed node, or create a list. The roster is not active until you `recluster`.
    :::
    
    Terminal window
    
    ```bash
    Admin+> asinfo -v "roster-set:namespace=test;nodes=BB9070016AE4202,BB9060016AE4202,BB9050016AE4202" with BB9020016AE4202
    
    node2.aerospike.com:3000 (192.168.10.2) returned:
    
    ok
    ```
    
    You now have a roster but it isn’t active yet.
    
4.  Validate your roster\* with the `roster:` command.
    
    Terminal window
    
    ```bash
    Admin+> asinfo -v "roster:"
    
    node2.aerospike.com:3000 (192.168.10.2) returned:
    
    ns=test:roster=null:pending_roster=BB9070016AE4202,BB9060016AE4202,BB9050016AE4202:observed_nodes=null
    
    node6.aerospike.com:3000 (192.168.10.6) returned:
    
    ns=test:roster=null:pending_roster=BB9070016AE4202,BB9060016AE4202,BB9050016AE4202:observed_nodes=null
    
    node4.aerospike.com:3000 (192.168.10.4) returned:
    
    ns=test:roster=null:pending_roster=BB9070016AE4202,BB9060016AE4202,BB9050016AE4202:observed_nodes=null
    ```
    
    Roster is null but pending\_roster is set with the provided roster.
    
5.  Apply the pending\_roster with the `recluster:` command.
    
    Terminal window
    
    ```bash
    Admin+> asinfo -v "recluster:"
    
    node2.aerospike.com:3000 (192.168.10.2) returned:
    
    ignored-by-non-principal
    
    node6.aerospike.com:3000 (192.168.10.6) returned:
    
    ignored-by-non-principal
    
    node4.aerospike.com:3000 (192.168.10.4) returned:
    
    ok
    ```
    
6.  Verify that the new roster was applied with the `roster:` command.
    
    Terminal window
    
    ```bash
    Admin+> asinfo -v "roster:"
    
    node2.aerospike.com:3000 (192.168.10.2) returned:
    
    ns=test:roster=BB9070016AE4202,BB9060016AE4202,BB9050016AE4202,BB9040016AE4202,BB9020016AE4202:pending_roster=BB9070016AE4202,
    
            BB9060016AE4202,BB9050016AE4202,BB9040016AE4202,BB9020016AE4202
    
    node6.aerospike.com:3000 (192.168.10.6) returned:
    
    ns=test:roster=BB9070016AE4202,BB9060016AE4202,BB9050016AE4202,BB9040016AE4202,BB9020016AE4202:pending_roster=BB9070016AE4202,
    
            BB9060016AE4202,BB9050016AE4202,BB9040016AE4202,BB9020016AE4202
    
    node4.aerospike.com:3000 (192.168.10.4) returned:
    
    ns=test:roster=BB9070016AE4202,BB9060016AE4202,BB9050016AE4202,BB9040016AE4202,BB9020016AE4202:pending_roster=BB9070016AE4202,
    
            BB9060016AE4202,BB9050016AE4202,BB9040016AE4202,BB9020016AE4202
    ```
    
    Both roster and pending\_roster are set to the provided roster.
    
7.  Validate that the namespace cluster size agrees with the service cluster size.
    
    The [`namespace`](https://aerospike.com/docs/database/reference/info?search=namespace#namespace) statistic `ns_cluster_size` should now agree with the service [`cluster_size`](https://aerospike.com/docs/database/reference/metrics#node_stats__cluster_size) assuming all nodes in the service have this namespace. When they do not, it could mean that either the namespace is not defined on all nodes, or nodes are missing from the roster.
    
    Terminal window
    
    ```bash
    Admin> show stat -flip like cluster_size
    
    ~~~~~~~~~~~~~~~~~~~~~~~~Service Statistics~~~~~~~~~~~~~~~~~~~~~
    
                              NODE            cluster_size
    
    node2.aerospike.com:3000                             5
    
    node4.aerospike.com:3000                             5
    
    node5.aerospike.com:3000                             5
    
    node6.aerospike.com:3000                             5
    
    node7.aerospike.com:3000                             5
    
    Number of rows: 5
    
    ~~~~~~~~~~~~~~~~~~~~~~~~test Namespace Statistics~~~~~~~~~~~~~~~~~~~~~
    
                              NODE            ns_cluster_size
    
    node2.aerospike.com:3000                             5
    
    node4.aerospike.com:3000                             5
    
    node5.aerospike.com:3000                             5
    
    node6.aerospike.com:3000                             5
    
    node7.aerospike.com:3000                             5
    
    Number of rows: 5
    ```
    

### Modifying the roster

[Managing data consistency](https://aerospike.com/docs/database/learn/strong-consistency) describes adding and removing nodes, starting and stopping servers safely, validating partition availability, and reviving dead partitions. Managing data consistency also describes the [`auto-revive`](https://aerospike.com/docs/database/learn/strong-consistency#auto-revive) feature, which was added in Database 7.1.0.

## Rack awareness

For an SC namespace to be rack aware, the roster list becomes a series of `node-id@rack-id` pairs. Each entry in the roster list needs to define which rack a node is on (defaulting to `rack-id 0` if none is defined). The roster can be manually constructed by appending `@rack-id` to each `node-id` in a comma-separated list.

Managing this list can be simplified by configuring [`rack-id`](https://aerospike.com/docs/database/reference/config#namespace__rack-id) on each node. These configured rack IDs automatically appear in the `observed_nodes` list, which can then be used as a roster list in the `set-roster` command.

::: note
The rack ID is specified in each namespace. It is possible to set different rack IDs for different namespaces, and it is possible to have some namespaces not be rack aware.
:::

Configure SC namespaces with rack awareness using the `rack-id` configuration to generate the `observed_nodes` list.

In SC mode, the `rack-id`configuration is only used to facilitate setting the roster by copying and pasting the `observed_nodes` list. Only the rack ID configured when setting the roster is applied, and it could be different than what has been configured in the configuration file or directly dynamically through the `rack-id` configuration parameter.

::: note
Starting with Database 7.2.0, the [active rack](https://aerospike.com/docs/database/reference/config#namespace__active-rack) feature dynamically designates a particular [`rack-id`](https://aerospike.com/docs/database/reference/config#namespace__rack-id) to hold all master partition copies. For instructions on how to enable active rack, see [Designate an active rack](https://aerospike.com/docs/database/manage/namespace/rack-aware#designate-an-active-rack).
:::

### Statically configure rack IDs

Modify the `rack-id` parameter for each _namespace_ in the `aerospike.conf` file.

Terminal window

```bash
namespace test {

   replication-factor 2

   memory-size 1G

   default-ttl 0

   strong-consistency true

   rack-id 101

   storage-engine device {

     file /var/lib/aerospike/test.dat

     filesize 4G

     data-in-memory false

     commit-to-device true

   }

}
```

### Dynamically assign observed nodes to racks

1.  Start the Aerospike server.
    
    Terminal window
    
    ```bash
    systemctl start aerospike
    ```
    
2.  Copy the observed nodes into the pending roster with asadm’s `manage roster` commands
    
    Terminal window
    
    ```bash
    Admin+> manage roster stage observed ns test
    ```
    
3.  View the roster with asadm’s `show roster` and notice that the Pending Roster has been updated.
    
4.  Apply the roster with asadm’s `manage recluster` command.
    
    Terminal window
    
    ```bash
    Admin+> manage recluster
    
    Successfully started recluster
    ```
    
5.  Verify the configured rack-ids are active with asadm’s `show racks` command., and that the displayed rack-id\_ matches what is configured.
    
    Terminal window
    
    ```bash
    Admin+> show racks
    
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Racks (2021-10-21 20:33:28 UTC)~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Namespace|Rack|                                                                          Nodes
    
            |  ID|
    
    test     |101 |BB9070016AE4202,BB9060016AE4202,BB9050016AE4202,BB9040016AE4202,BB9020016AE4202
    
    Number of rows: 1
    ```
    

The cluster is now configured with rack awareness.

### Dynamically reassign nodes to racks

1.  Dynamically set rack-id with asadm’s `manage config` command:
    
    Terminal window
    
    ```bash
    Admin+> manage config namespace test param rack-id to 101 with 192.168.10.2 192.168.10.4 192.168.10.5
    
    ~Set Namespace Param rack-id to 101~
    
                        Node|Response
    
    node2.aerospike.com:3000|ok
    
    node4.aerospike.com:3000|ok
    
    node5.aerospike.com:3000|ok
    
    Number of rows: 3
    
    Admin+> manage config namespace test param rack-id to 102 with 192.168.10.6 192.168.10.7
    
    ~Set Namespace Param rack-id to 102~
    
                        Node|Response
    
    node6.aerospike.com:3000|ok
    
    node7.aerospike.com:3000|ok
    
    Number of rows: 2
    ```
    
2.  Issue a `recluster` with asadm’s `manage recluster` command.
    
    Terminal window
    
    ```bash
    Admin+> manage recluster
    
    Successfully started recluster
    ```
    

### Rack aware reads

Rack awareness also provides a mechanism for database clients to read from the servers in the closest rack or zone on a preferential basis. This can result in lower latency, increased stability, and significantly reduced traffic charges by limiting cross-availability-zone traffic.

1.  Set up clusters in logical racks. (See [Configure rack awareness](https://aerospike.com/docs/database/manage/namespace/consistency/#rack-awareness)
    
2.  Set the `rackId` and `rackAware` flags in the `ClientPolicy` object. Use the rack ID specified in the nodes for the associated-AZ where that application is running. The following example uses Java to demonstrate how to enable rack awareness. Commands are similar in other clients.
    
    ```java
    ClientPolicy clientPolicy = new ClientPolicy();
    
    clientPolicy.rackId = <<rack id>>;
    
    clientPolicy.rackAware = true;
    ```
    
    ::: note
    To avoid hard-coding, the rack ID can be obtained dynamically using the cloud provider’s API, or set in a local property file.
    :::
    
3.  Once the application has connected, set 2 additional parameters in the policy associated with the reads to be rack aware.
    
    ```java
    Policy policy = new Policy();
    
    policy.readModeSC = ReadModeSC.ALLOW_REPLICA;
    
    policy.replica = Replica.PREFER_RACK;
    
    readModeSC.ALLOW_REPLICA indicates that all replicas can be consulted.
    
    policy.replica = Replica.PREFER_RACK indicates that the record in the same rack should be accessed if possible.
    ```
    
    ::: tip
    -   These parameters are additional to any other policy flags such as timeouts and retry intervals.
    -   It is a best practice to set the reads to time out after a reasonable duration, such as 50ms, and have Aerospike automatically retry.
    -   The retry is usually on a different node from the first read, giving more resilient reads in the face of a node failure.
    -   If the node the client is reading from fails during the read, the retry moves to a different node in a different AZ with rack awareness set up, which will most likely still be there.
    :::
    

## Designate an active rack

Active rack dynamically designates a particular `rack-id` to hold all master partition copies. For `active-rack` to take effect, all nodes must agree on the same active rack, and the number of racks must be at most equal to the configured [`replication-factor`](https://aerospike.com/docs/database/reference/config#namespace__replication-factor).

Also, `active-rack = 0` disables the feature. This means that you can’t designate `rack_id` 0 as the active rack.

Changing the `rack_id` on all nodes with `rack_id` 0 to a new value that is distinct from any other racks does not cause any migrations.

### Enable active rack for SC statically

In SC mode, the information about the active rack must be communicated with the roster. The roster should be applied when the cluster is stable. Having these values on the roster ensures that the roster nodes, racks, and active rack agree on all nodes, even if the cluster is later split into subclusters by network partitions.

Use the following steps to enable active rack on a SC namespace.

1.  Static configuration of the namespace.
    
    ```asciidoc
    namespace cp {
    
      nsup-period 120
    
      default-ttl 5d
    
      replication-factor 2
    
        rack-id 1 # set rack-id
    
        strong-consistency true
    
        active-rack 1 # set active-rack
    
      storage-engine memory {
    
        data-size 2G
    
        evict-used-pct 60
    
      }
    
    }
    ```
    
    Initial output for `show pmap`
    
    ```asciidoc
    Admin+> show pmap
    
    ~~~~~~~~~~~~~Partition Map Analysis (2024-07-26 17:30:10 UTC)~~~~~~~~~~~~~
    
    Namespace|            Node| Cluster Key|~~~~~~~~~~~~Partitions~~~~~~~~~~~~
    
             |                |            |Primary|Secondary|Unavailable|Dead
    
    cp       |172.22.22.1:3000|3ABD3A9B0390|    682|      683|          0|   0
    
    cp       |172.22.22.2:3000|3ABD3A9B0390|    682|      683|          0|   0
    
    cp       |172.22.22.3:3000|3ABD3A9B0390|    683|      682|          0|   0
    
    cp       |172.22.22.4:3000|3ABD3A9B0390|    683|      682|          0|   0
    
    cp       |172.22.22.5:3000|3ABD3A9B0390|    683|      683|          0|   0
    
    cp       |172.22.22.6:3000|3ABD3A9B0390|    683|      683|          0|   0
    
    cp       |                |            |   4096|     4096|          0|   0
    
    Number of rows: 6
    ```
    
2.  Re-roster and recluster
    
    ```asciidoc
    Admin> enable
    
    Admin+> manage roster stage observed ns cp
    
    Pending roster now contains observed nodes.
    
    Run "manage recluster" for your changes to take effect.
    
    Admin+> manage recluster
    ```
    
3.  Verify that migrations have completed:
    
    ```asciidoc
    Admin+> info namespace object
    
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Namespace Object Information (2024-07-26 17:30:20 UTC)~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Namespace|            Node|Rack|  Repl|Expirations|  Total|~~~~~~~~~~Objects~~~~~~~~~~|~~~~~~~~~Tombstones~~~~~~~~|~~~~Pending~~~~
    
             |                |  ID|Factor|           |Records| Master|  Prole|Non-Replica| Master|  Prole|Non-Replica|~~~~Migrates~~~
    
             |                |    |      |           |       |       |       |           |       |       |           |     Tx|     Rx
    
    cp       |172.22.22.1:3000|   1|     2|    0.000  |0.000  |0.000  |0.000  |    0.000  |0.000  |0.000  |    0.000  |0.000  |0.000
    
    cp       |172.22.22.2:3000|   1|     2|    0.000  |0.000  |0.000  |0.000  |    0.000  |0.000  |0.000  |    0.000  |0.000  |0.000
    
    cp       |172.22.22.3:3000|   1|     2|    0.000  |0.000  |0.000  |0.000  |    0.000  |0.000  |0.000  |    0.000  |0.000  |0.000
    
    cp       |172.22.22.4:3000|   2|     2|    0.000  |0.000  |0.000  |0.000  |    0.000  |0.000  |0.000  |    0.000  |0.000  |0.000
    
    cp       |172.22.22.5:3000|   2|     2|    0.000  |0.000  |0.000  |0.000  |    0.000  |0.000  |0.000  |    0.000  |0.000  |0.000
    
    cp       |172.22.22.6:3000|   2|     2|    0.000  |0.000  |0.000  |0.000  |    0.000  |0.000  |0.000  |    0.000  |0.000  |0.000
    
    cp       |                |    |      |    0.000  |0.000  |0.000  |0.000  |    0.000  |0.000  |0.000  |    0.000  |0.000  |0.000
    
    Number of rows: 6
    ```
    
4.  Verify `show pmap` shows `active-rack` nodes have the primary partitions.
    
    ```asciidoc
    Admin+> show pmap
    
    ~~~~~~~~~~~~~Partition Map Analysis (2024-07-26 17:30:25 UTC)~~~~~~~~~~~~~
    
    Namespace|            Node| Cluster Key|~~~~~~~~~~~~Partitions~~~~~~~~~~~~
    
             |                |            |Primary|Secondary|Unavailable|Dead
    
    cp       |172.22.22.1:3000|7320E4F4EE63|   1365|        0|          0|   0
    
    cp       |172.22.22.2:3000|7320E4F4EE63|   1365|        0|          0|   0
    
    cp       |172.22.22.3:3000|7320E4F4EE63|   1366|        0|          0|   0
    
    cp       |172.22.22.4:3000|7320E4F4EE63|      0|     1365|          0|   0
    
    cp       |172.22.22.5:3000|7320E4F4EE63|      0|     1365|          0|   0
    
    cp       |172.22.22.6:3000|7320E4F4EE63|      0|     1366|          0|   0
    
    cp       |                |            |   4096|     4096|          0|   0
    
    Number of rows: 6
    ```
    
    All master (or “primary”) partitions are now on the nodes that were designated `rack-id 1`.
    

### Change active rack for SC dynamically

1.  Set active rack dynamically
    
    ```asciidoc
    Admin+> manage config namespace ns-name param active-rack to 2
    ```
    
2.  re-cluster to set the active rack
    
    ```asciidoc
    Admin+> manage recluster
    ```
    
3.  re-roster and re-cluster again to apply active rack
    
    ```asciidoc
    Admin+> manage roster stage observed ns cp
    
    Pending roster now contains observed nodes.
    
    Run "manage recluster" for your changes to take effect.
    
    Admin+> manage recluster
    ```
    
4.  Verify `show pmap` shows `active-rack` nodes have the primary partitions.
    
    ```asciidoc
    Admin+> show pmap
    
    ~~~~~~~~~~~~~Partition Map Analysis (2024-07-26 17:30:25 UTC)~~~~~~~~~~~~~
    
    Namespace|            Node| Cluster Key|~~~~~~~~~~~~Partitions~~~~~~~~~~~~
    
             |                |            |Primary|Secondary|Unavailable|Dead
    
    cp       |172.22.22.1:3000|7320E4F4EE63|      0|     1365|          0|   0
    
    cp       |172.22.22.2:3000|7320E4F4EE63|      0|     1365|          0|   0
    
    cp       |172.22.22.3:3000|7320E4F4EE63|      0|     1366|          0|   0
    
    cp       |172.22.22.4:3000|7320E4F4EE63|   1365|        0|          0|   0
    
    cp       |172.22.22.5:3000|7320E4F4EE63|   1365|        0|          0|   0
    
    cp       |172.22.22.6:3000|7320E4F4EE63|   1366|        0|          0|   0
    
    cp       |                |            |   4096|     4096|          0|   0
    
    Number of rows: 6
    ```
    

## Configure SC for expiration

SC should be used carefully with expiration. For background on expiration and eviction, see [Definition of expiration and eviction](https://aerospike.com/docs/database/manage/namespace/retention/#expirations-evictions-and-ttl).

For each namespace where you want SC, add `strong-consistency true` and `default-ttl 0` to the namespace stanza. This configuration requires Database 7.0.0 or later.

Terminal window

```bash
namespace test {

    replication-factor 2

    default-ttl 0

    strong-consistency true

    storage-engine memory {

       file /var/lib/aerospike/test.dat

       filesize 4G

    }

}
```

### Non-durable deletes and configuration settings

A key consideration for SC is the length of time records exist, which is a function of several configuration parameters.

If a record is non-durably deleted in one master partition but has not yet been consistently marked as deleted in another partition, when the master has to heal by restoring a prior replica, the “deleted” record is restored in the live partition.

Verify that when expunge, expiration, or eviction of non-durable-delete events occur, no transactions are updating the record. With [`strong-consistency-allow-expunge`](https://aerospike.com/docs/database/reference/config#namespace__strong-consistency-allow-expunge) `true`, for highly active or essential records, you have the following options:

1.  Set the [`default-ttl`](https://aerospike.com/docs/database/reference/config#namespace__default-ttl) parameter far enough into the future to be reasonably confident that updates do not occur during expiration. For example, `default-ttl 365D` sets the TTL to 365 days, or one year.
    
2.  Disable eviction with the parameters:
    
    1.  [`high-water-memory-pct`](https://aerospike.com/docs/database/reference/config#namespace__high-water-memory-pct) `0`.
        
    2.  [`high-water-disk-pct`](https://aerospike.com/docs/database/reference/config#namespace__high-water-disk-pct) `0`.
        
    3.  [`mounts-high-water-pct`](https://aerospike.com/docs/database/reference/config#namespace__mounts-high-water-pct) `0`.
        

## Commit-to-device

Determine whether you need `commit-to-device`. If you are running in a situation where no data loss is acceptable even in the case of simultaneous server hardware failures, you can choose that a namespace commits to disk. This will cause performance degradation, and only provides benefit where hardware failures are within milliseconds of each other. Add `commit-to-device true` within the storage engine scope of the namespaces in question.

`commit-to-device` requires serializing writes to the output buffer, and will thus flush more data than is strictly necessary. Although Aerospike automatically determines the smallest flush increment for a given drive, this can be raised with the optional `commit-min-size` parameter.

Start the servers.

Terminal window

```bash
systemctl start aerospike
```

The cluster forms with all nodes but without a per-roster namespace. To use your SC namespace, you must add the roster. Until you do, client requests will fail.

Terminal window

```bash
Admin> show stat -flip like cluster_size

~~~~~~~~~~~~~~~~~~~~~~~~Service Statistics~~~~~~~~~~~~~~~~~~~~~

                          NODE            cluster_size

node2.aerospike.com:3000                             5

node4.aerospike.com:3000                             5

node5.aerospike.com:3000                             5

node6.aerospike.com:3000                             5

node7.aerospike.com:3000                             5

Number of rows: 5

~~~~~~~~~~~~~~~~~~~~~~~~test Namespace Statistics~~~~~~~~~~~~~~~~~~~~~

                          NODE            ns_cluster_size

node2.aerospike.com:3000                             0

node4.aerospike.com:3000                             0

node5.aerospike.com:3000                             0

node6.aerospike.com:3000                             0

node7.aerospike.com:3000                             0

Number of rows: 5
```

This result is expected, since the `test` namespace’s roster has not yet been modified.

## Install and configure clock synchronization

Aerospike recommends using a clock synchronization system compatible with your environment. The most common method of synchronizing clocks is the common NTP protocol, which easily exceeds the granularity that Aerospike requires.

-   Aerospike’s gossip heartbeat protocol monitors the amount of skew in a cluster, and sends an alert if it detects a large amount of skew.
-   10 seconds or fewer of skew is well within acceptable limits and does not trigger any warnings.
-   By default, warnings begin at 12 seconds of skew to provide early notification before conditions worsen.
-   By default, the database enters stop-writes mode at 17 seconds of skew to prevent data loss.
-   Data loss is possible at 23 seconds or more of skew with the default heartbeat configuration.

For information on installing NTP, see [How to configure NTP for Aerospike](https://support.aerospike.com/s/article/How-to-configure-ntp-for-Aerospike).