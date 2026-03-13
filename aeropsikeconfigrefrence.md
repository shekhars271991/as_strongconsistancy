# Configuration reference

This page is a complete list of Aerospike Database configuration options. A carefully planned and optimized database configuration is essential to running a successful Aerospike deployment. To learn more, see the main [database configuration documentation](https://aerospike.com/docs/database/manage/database/as-config). The Aerospike configuration file is located by default at `/etc/aerospike/aerospike.conf`.

Configuration options listed by default are available to the most recent Aerospike database version. To see options available to other database versions, select your version from the `Version` dropdown menu.

Be sure to review the [dynamic runtime configuration](https://aerospike.com/docs/database/tools/runtime-config) examples.

 

## Logging

#### `console`

`static`

Context: logging

Description: A Linux console log sink. A systemd Linux OS captures the log stream from STDERR to journald. In SysV Linux the default `console` sink is `/tmp/aerospike-console.<pid>`.

Introduced: \-

Removed: \-

Default Value: \-

Detail:
A `console` log sink subcontext can have one or more `context` configuration parameters.

You can obtain the [logging contexts](https://aerospike.com/docs/database/manage/logging/logs#logging-contexts) and [severity level](https://aerospike.com/docs/database/manage/logging/logs#severity-level-details) associated with a specified log sink with an info command:

```asciidoc
asinfo -v log/0
```

Returns the values associated with the first log sink defined in `logging`:

```asciidoc
misc:CRITICAL;alloc:CRITICAL;arenax:CRITICAL;hardware:CRITICAL;jem:CRITICAL;msg:CRITICAL;...
```

To list the log sinks:

```asciidoc
asinfo -v log/0
```

Prior to Aerospike Database 4.9.0, the default value was `any info`, for an INFO severity level. For common log messages, organized by logging context, see [Log message reference](https://aerospike.com/docs/database/reference/logs).

**Example:**

```asciidoc
logging {

    console {

        context any info

    }

}
```

---

#### `context`

`dynamic`

Context: logging

Subcontext: file, console, or syslog

Description: Specifies the [logging contexts](https://aerospike.com/docs/database/manage/logging/logs#logging-contexts) and [severity level](https://aerospike.com/docs/database/manage/logging/logs#severity-level-details) to filter a log stream. You can use a combination of contexts and severity levels. See [Change the severity level dynamically](https://aerospike.com/docs/database/manage/logging/logs#change-the-severity-level-dynamically).

Introduced: \-

Removed: \-

Default Value: any critical

Detail:
The logging contexts and the severity levels associated with a specified log sink can be obtained with an info command, where 0 is the sink-id:

```asciidoc
asinfo -v log/0
```

Returns the values associated with the first log sink defined in `logging`:

```asciidoc
misc:CRITICAL;alloc:CRITICAL;arenax:CRITICAL;hardware:CRITICAL;jem:CRITICAL;msg:CRITICAL;...
```

To list the log sinks:

```asciidoc
asinfo -v "logs" -l
```

Prior to Aerospike Database 4.9.0, the default value was `any info`, for an INFO severity level. For common log messages, organized by logging context, see [Log message reference](https://aerospike.com/docs/database/reference/logs).

---

#### `facility`

`static`

Context: logging

Subcontext: syslog

Description: Specifies the standard syslog facility name to be used when logging to a syslog socket.

Introduced: 6.3.0

Removed: \-

Default Value: local0

Detail:
See [Configuring Log Streams](https://aerospike.com/docs/database/manage/logging/logs).

---

#### `file`

`static`

Context: logging

Description: Defines a file log sink (not to be confused with `file` from the namespace configuration context.) You can define multiple log sinks for various contexts.

Introduced: \-

Removed: \-

Default Value: /var/log/aerospike/aerospike.log

Detail:
A `file` log sink subcontext can have one or more `context` configuration parameters.

Context specifies the [logging contexts](https://aerospike.com/docs/database/manage/logging/logs#logging-contexts) and [severity level](https://aerospike.com/docs/database/manage/logging/logs#severity-level-details) used to filter messages in the log stream. You can use a combination of contexts and severity levels.

**Example:**

```asciidoc
logging {

    file /var/log/aerospike/aerospike.log {

        context any critical

    }

    file /var/log/aerospike/udf_debug.log {

        context any critical

        context udf debug

    }

}
```

---

#### `path`

`static`

Context: logging

Subcontext: syslog

Description: Specifies a valid path to a syslog compatible Unix domain socket.

Introduced: 6.3.0

Removed: \-

Default Value: /dev/log

Detail:
See [Configuring Log Streams](https://aerospike.com/docs/database/manage/logging/logs).

---

#### `syslog`

`static`

Context: logging

Description: Defines a pre-existing syslog-compatible Unix domain socket as a log sink.

Introduced: 6.3.0

Removed: \-

Default Value: \-

Detail:
A `syslog` log sink subcontext can have the following configuration parameters: `facility`, `tag`, `path`, and one or more `context`.

Context specifies the [logging contexts](https://aerospike.com/docs/database/manage/logging/logs#logging-contexts) and [severity level](https://aerospike.com/docs/database/manage/logging/logs#severity-level-details) used to filter messages in the log stream. You can use a combination of contexts and severity levels.

**Example:**

```asciidoc
logging {

    syslog {

        facility local0

        tag asd-query

        context any critical

        context query info

    }

}
```

---

#### `tag`

`static`

Context: logging

Subcontext: syslog

Description: Specifies a syslog tag to be used for labeling messages going to the socket log sink.

Introduced: 6.3.0

Removed: \-

Default Value: asd

Detail:
See [Log management](https://aerospike.com/docs/database/manage/logging/logs).

---

## Mod lua

#### `cache-enabled`

`static`

Context: mod-lua

Description: Whether to enable caching of Lua states for each registered Lua module, to benefit performance.

Introduced: \-

Removed: \-

Default Value: true

Detail:
With the cache enabled, 10 Lua states are initially cached for each Lua module on every node, and the cache expands as needed at runtime up to a maximum of 128 entries per module.

---

#### `user-path`

`static`

Context: mod-lua

Description: Directory to be used by the Aerospike process to store user generated UDF files.

Introduced: \-

Removed: \-

Default Value: /opt/aerospike/usr/udf/lua

Detail:
If this directory is user specified, the Aerospike process must have read/write permission on that directory.

---

## Namespace

#### `active-rack`

`enterprise` `dynamic` `cloud`

Context: namespace

Description: Enables operator to dynamically designate a particular [`rack-id`](https://aerospike.com/docs/database/reference/config#namespace__rack-id) to hold all master partition copies. For `active-rack` to take effect, all nodes must agree on the same active rack, and the number of racks must be less than or equal to the configured [`replication-factor`](https://aerospike.com/docs/database/reference/config#namespace__replication-factor). Also, `active-rack = 0` (default) disables the feature. This means that you can’t designate `rack_id` 0 as the active rack. Changing the `rack_id` on all nodes with `rack_id` 0 to a new value that is distinct from any other racks, does not cause any migrations.

Introduced: 7.2.0

Removed: \-

Default Value: 0

Detail:
**Example:**

Enable using `aerospike.conf`

```asciidoc
namespace ns-name {

...

rack-id X

active-rack Y #Y may be the same as X"

...
```

---

#### `allow-nonxdr-writes`

`dynamic`

Context: namespace

Description: In Aerospike 5.0.0, this parameter was replaced by [`reject-non-xdr-writes`](https://aerospike.com/docs/database/reference/config#namespace__reject-non-xdr-writes). Parameter to control the writes done by a non-XDR client. Setting it to false will disallow all the writes from a non-XDR client (any regular client library). This parameter is useful to control accidental writes by a non-XDR client to a namespace when it is not expected, and can be used for namespaces taking writes exclusively from XDR client(s). When set to false, error code 10 will be returned and will tick the [`fail_xdr_forbidden`](https://aerospike.com/docs/database/reference/metrics#namespace__fail_xdr_forbidden) statistic.

Introduced: 3.5.12

Removed: 5.0.0

Default Value: true

Detail:
**Example:** Set allow-nonxdr-writes to false:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;allow-nonxdr-writes=false"
```

---

#### `allow-ttl-without-nsup`

`dynamic` `cloud`

Context: namespace

Description: Aerospike strongly recommends that you do not change this setting. See the **Warning** in “Additional Information” below.  
  
If data expiration and eviction are disabled ([nsup-period](https://aerospike.com/docs/database/reference/config#namespace__nsup-period) set to 0, the default), setting `allow-ttl-without-nsup` to `true` allows writes of records with a non-zero TTL (which would otherwise will not be allowed).

Introduced: 4.9.0

Removed: \-

Default Value: false

Detail:
**Example:** Set `allow-ttl-without-nsup` to true:

```plaintext
asinfo -v "set-config:context=namespace;namespace=namespaceName;allow-ttl-without-nsup=true"
```

For additional discussion, see [Namespace Data Retention Configuration](https://aerospike.com/docs/database/manage/namespace/retention).

Aerospike strongly recommends that you not change this setting.  
  
_The server will not start_ if `nsup-period` is 0 (the default) but [`default-ttl`](https://aerospike.com/docs/database/reference/config#namespace__default-ttl) is non-zero, unless if this setting is set to `true`.

---

#### `allow-xdr-writes`

`dynamic`

Context: namespace

Description: In Aerospike 5.0.0, this parameter was replaced by [`reject-xdr-writes`](https://aerospike.com/docs/database/reference/config#namespace__reject-xdr-writes). Parameter to control whether to accept write transactions originating from an XDR client. Setting it to false will disallow all the writes from an XDR client (at a destination cluster) and will only allow non XDR clients to write transactions. This parameter is useful to control accidental writes by an XDR client. When set to false, error code 10 will be returned, disallowed writes will not be relogged by XDR and will tick the [`fail_xdr_forbidden`](https://aerospike.com/docs/database/reference/metrics#namespace__fail_xdr_forbidden) statistic on the remote (destination) cluster.

Introduced: 3.5.12

Removed: 5.0.0

Default Value: true

Detail:
**Example:** Set allow-xdr-writes to true:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;allow-xdr-writes=true"
```

---

#### `apply-ttl-reduction`

`enterprise` `dynamic` `cloud`

Context: namespace

Description: Blocks client writes from reducing a record’s time-to-live (TTL). Updates are counted by the metrics [`ttl_reductions_applied`](https://aerospike.com/docs/database/reference/metrics/#namespace__ttl_reductions_applied) and [ttl\_reductions\_ignored](https://aerospike.com/docs/database/reference/metrics/#namespace__ttl_reductions_ignored) Records where the TTL was reduced could potentially lead to zombie records being resurrected by a cold restart. See [Avoiding zombie records](https://aerospike.com/docs/database/manage/namespace/retention/#avoiding-zombie-records).

Introduced: 8.1.0

Removed: \-

Default Value: true

Detail:
**Example:**

Enable using `aerospike.conf`

```asciidoc
namespace ns-name {

...

apply-ttl-reduction false

...
```

---

#### `auto-revive`

`enterprise` `static` `cloud`

Context: namespace

Description: Selectively revives partitions in SC namespaces at startup. The revive command forces a partition to go “live” and start accepting transactions providing the operations team an opportunity to take remediation actions when a series of events may have caused data loss.

The auto-revive feature is for deployments that don’t have any remediation options available and/or want to minimize downtime due to potential data loss. The auto-revive feature is selective; it will only revive partitions that have data, whereas the revive command will also revive partitions that have been totally lost (such as wiped disks on multiple nodes).

Introduced: 7.1.0

Removed: \-

Default Value: false

Detail:
In a case where two nodes in a strong-consistency replication-factor 2 namespace were shut down uncleanly, using SIGKILL for instance, the cluster detects possible lost data resulting in dead partitions. Without auto-revive, the operator follows remediation steps, including issuing the revive command to the cluster.

With the auto-revive feature enabled, the cluster ignores this potential data loss event and continues to allow client traffic. However, if the two nodes in this scenario had their data wiped, then the auto-revive feature would not restore the affected partitions and would still require that the operator take remediation steps, including issuing the revive command.

Example configuration:

```plaintext
namespace test {

...

auto-revive true

...
```

---

#### `background-query-max-rps`

`dynamic` `cloud`

Context: namespace

Description: Maximum records per second (RPS) allowed for a background query such as a UDF or ops query. If necessary, the query is throttled so as to not exceed this RPS value. Value range: 1-1000000. If the query must read the records from device to do any filtering (bin level filters), or if it reads them from device with no filtering, the throttle is applied to the rate at which records are read. If the records are stored in memory, or can be filtered based on index metadata, the throttle is applied to the rate at which the records are returned to the client.

Introduced: 6.0.0

Removed: \-

Default Value: 10000

Detail:
**Example:** Set background-query-max-rps to 6000:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;background-query-max-rps=6000"
```

This throttling applies only to background or UDF queries. The value of this parameter at query start time is used for the life of the query; dynamic changes are not applied to queries that are already running. For throttling of basic query specific client policy settings should be used. These are described in the applicable Client API doc under Query Policy.

---

#### `background-scan-max-rps`

`dynamic`

Context: namespace

Description: Maximum records per second (RPS) allowed for a background scan such as UDF or ops scan. If necessary, the scan is throttled so as to not exceed this RPS value. Value range: 1-1000000. If the scan must read the records from device to do any fbin level filters, or if it reads them from device with no filtering, the throttle is applied to the rate at which records are read. If the records are stored in memory,or can be filtered based on index metadata, the throttle is applied to the rate at which the records are returned to the client.

Introduced: 4.7.0

Removed: 6.0.0

Default Value: 10000

Detail:
**Example:** Set background-scan-max-rps to 6000:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;background-scan-max-rps=6000"
```

As the name suggests, this throttling applies only to background or UDF scans. For throttling of basic scan specific client policy settings should be used. These are described in the applicable Client API doc under Scan Policy.

This parameter was renamed to [`background-query-max-rps`](https://aerospike.com/docs/database/reference/config#namespace__background-query-max-rps) in Database 6.0.0

---

#### `cache-replica-writes`

`dynamic` `cloud`

Context: namespace

Subcontext: storage-engine device

Description: Controls whether replica writes are placed into the post-write queue. Setting this true could improve performance in certain situations. It cannot be set true for [`data-in-memory`](https://aerospike.com/docs/database/reference/config#namespace__data-in-memory) namespaces.

Introduced: 4.8.0

Removed: \-

Default Value: false

Detail:
We recommend that you set this to `true` when using client [rack-aware](https://aerospike.com/docs/database/learn/architecture/clustering/rack-aware), or when using random read mode with [`replication-factor`](https://aerospike.com/docs/database/reference/config#namespace__read-page-cache) `all`.

---

#### `cold-start-empty`

`static` `cloud`

Context: namespace

Subcontext: storage-engine device

Description: Setting this to true will cause cold start to ignore existing data on drives and start as if empty. Does not affect [fast restart](https://aerospike.com/docs/database/manage/database/fast-start).

Introduced: 3.3.21

Removed: \-

Default Value: false

Detail:
May be used to avoid deleted objects reappearing upon cold start. After restart, migrates will replicate data back to this node.

Before cold-starting another node, make sure migrations have completed to avoid any data loss.

---

#### `commit-min-size`

`enterprise` `static`

Context: namespace

Subcontext: storage-engine device

Description: Minimum size, in bytes, of a disk flush when [`commit-to-device`](https://aerospike.com/docs/database/reference/config#namespace__commit-to-device) is enabled. Has to be a power of 2. Can be set as 4K. The default value of 0 will auto-detect the smallest size possible for the device. It is usually recommended to keep the default for this configuration.

Introduced: 4.0.0

Removed: 7.0.0

Default Value: 0

Detail:
Supported size notation is no suffix for bytes, K for Kibibyte (KiB).

See [Finding total namespace memory](https://aerospike.com/docs/database/observe/key-metrics#finding-total-namespace-memory) for the total memory accounted for the namespace.

---

#### `commit-to-device`

`enterprise` `static` `cloud`

Context: namespace

Subcontext: storage-engine device or storage-engine pmem or storage-engine memory

Description: Wait for write to flush to disk or pmem before acknowledging the client. Only available for [`strong-consistency`](https://aerospike.com/docs/database/reference/config#namespace__strong-consistency) enabled namespaces. If using `storage-engine device` file storage with `commit-to-device` set `true`, it may be useful to set [`read-page-cache`](https://aerospike.com/docs/database/reference/config#namespace__read-page-cache) `true`.

Introduced: 4.8.0 (pmem) 7.0.0 (storage-engine memory)

Removed: \-

Default Value: false

Detail:
In case of a crash, when running with `commit-to-device` set to true, all partitions will be trusted upon the subsequent cold start.

When using [shadow devices](https://aerospike.com/docs/database/manage/namespace/storage/config/#setup-for-shadow-device), this setting will commit to both primary and shadow prior to returning to the client and will therefore likely slow transaction latencies even further.

Having more physical or logical devices can help avoid potential bottlenecks caused by the serialization on the write buffer.

---

#### `compression-acceleration`

`enterprise` `dynamic` `cloud`

Context: namespace

Subcontext: storage-engine device or storage-engine pmem or storage-engine memory

Description: This parameter sets an acceleration level for LZ4 storage compression. Lower values specify lower acceleration, resulting in higher compression levels and greater CPU usage. The allowable range is 1 - 65537, with a default value of 1, indicating no acceleration and maximum compression. In practice, values greater than 400 result in no compression.

Only applicable when [`compression`](https://aerospike.com/docs/database/reference/config#namespace__compression) is set to `lz4`.

Introduced: 6.3.0 7.0.0 (storage-engine memory)

Removed: \-

Default Value: 1

Detail:
**Example:** Set `compression-acceleration` dynamically to 50:

```asciidoc
asinfo -v 'set-config:context=namespace;namespace=nameSpaceName;compression-acceleration=50'
```

---

#### `compression-level`

`enterprise` `dynamic` `cloud`

Context: namespace

Subcontext: storage-engine device or storage-engine pmem or storage-engine memory

Description: **Note**: This is `compression-level` for `storage-engine`. For XDR `compression-level` for `dc` `namespace`, scroll down to `compression-level` in the XDR context.

Allowable range: 1-9

The compression level to use with ZSTD compression. Controls the trade-off between compression speed and compression ratio. A higher level value, for example `9`, means more efficient but slower compression. A lower level value, for example `1`, means less efficient but faster compression. This item should only be specified when using `compression zstd`.  
  
In Aerospike Database prior to 4.6.x, if this setting has never been specified when using `compression zstd`, a default flag of 0 is displayed and the compression-level of 9 is used.

In Aerospike Database 4.6.0.x or later, if this setting has never been specified when using `compression zstd`, a default flag of 9 is displayed and the compression-level of 9 is used.  
  
The [compression configuration directives](https://aerospike.com/docs/database/manage/namespace/storage/compression#configuration) belong to a namespace’s storage-engine section.

Introduced: 4.5.0 (device) 4.8.0 (pmem) 7.0.0 (storage-engine memory)

Removed: \-

Default Value: 0

Detail:
**Example:** Set the namespace’s compression-level to 1:

```plaintext
asinfo -v 'set-config:context=namespace;namespace=namespaceName;compression-level=1'
```

`id=` is deprecated in `set-config` Database 7.2.0 replaced with `namespace=`.:::

---

#### `compression`

`enterprise` `dynamic` `cloud`

Context: namespace

Subcontext: storage-engine device or storage-engine pmem or storage-engine memory

Description: Options: none, lz4, snappy, zstd.

Use of compression requires the `asdb-compression` feature-key to be enabled in the [`feature-key-file`](https://aerospike.com/docs/database/reference/config#service__feature-key-file), and specifies the algorithm used to [compress records](https://aerospike.com/docs/database/manage/namespace/storage/compression) on SSD or pmem storage files. For `zstd` the [`compression-level`](https://aerospike.com/docs/database/reference/config#namespace__compression-level) can be specified.  
  
As of Database 4.5.3.2, the flat storage format is also used as wire format for replication, migration and duplicate resolution, providing potential significant network bandwidth and CPU usage when using compression.

Introduced: 4.5.0 (device) 4.8.0 (pmem) 7.0.0 (storage-engine memory)

Removed: \-

Default Value: none

Detail:
**Example:** Set the namespace’s compression algorithm to zstd:

```plaintext
asinfo -v 'set-config:context=namespace;namespace=namespaceName;compression=zstd'
```

Compression does not allow to write records larger than the configured write block size (which is fixed at 8 MB for pmem), even if their compressed sizes would be smaller than the write block size. Compression happens at the storage and fabric layer. Using different compression options on different nodes for benchmarking purposes is supported.

---

#### `conflict-resolution-policy`

`dynamic` `cloud`

Context: namespace

Description: Set to either _last-update-time_ or _generation_

_generation_ - Resolve records conflict based on the record’s generation number.

_last-update-time_ - Resolve records conflict based on the record’s last update time.

This parameter does not impact the cold restart conflict resolution policy. Cold restart conflict resolution always uses the `last-update-time`. For records created prior to Database 3.8.3, the cold start resolution falls back to `generation`. Also, in case of equal `last-update-time`, the tie is broken by generation.

Introduced: \-

Removed: \-

Default Value: generation

Detail:
Generation value could wrap back to 1 on a record with a high update rate (Max of 65K generations per record). In AP mode ([`strong-consistency`](https://aerospike.com/docs/database/reference/config#namespace__strong-consistency) set to false) network partitions could cause updates to be lost when the cluster re-forms itself. Where it is more important to preserve the history of a record (such as lists or maps with items appended on each update) `generation` may be more suitable. Where the last update is more important to preserve, `last-update-time` would be more suitable.

**Example:** Set `conflict-resolution-policy` to last-update-time:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;conflict-resolution-policy=last-update-time"
```

Not configurable when [`strong-consistency`](https://aerospike.com/docs/database/reference/config#namespace__strong-consistency) is enabled (neither generation nor only last-update-time is in such case but a combination of last-update-time and regime).

`id=` is deprecated in `set-config` Database 7.2.0 replaced with `namespace=`.:::

---

#### `conflict-resolve-writes`

`enterprise` `dynamic` `cloud`

Context: namespace

Description: `conflict-resolve-writes` is required for the XDR bin convergence feature. If this is enabled, the bin-level LUT is stored and determines the winner. If this is disabled, the bin-level LUT is discarded and the latest write cannot be determined. `conflict-resolve-writes` cannot be enabled if `single-bin` is enabled for the namespace. See [bin convergence](https://aerospike.com/docs/database/manage/xdr/convergence) for more information.

Introduced: 5.4.0

Removed: \-

Default Value: false

Detail:
**Example:** Set conflict-resolve-writes dynamically:

```plaintext
asinfo -v "set-config:context=namespace;namespace=namespaceName;conflict-resolve-writes=true"
```

`id=` is deprecated in `set-config` Database 7.2.0 replaced with `namespace=`.:::

---

#### `data-in-index`

`unanimous` `static`

Context: namespace

Description: Optimization in single bin case, will only allow integer or float stored in index space. Can only be used when [`storage-engine`](https://aerospike.com/docs/database/reference/config#namespace__storage-engine) is device and [`single-bin`](https://aerospike.com/docs/database/reference/config#namespace__single-bin) is true.

Introduced: \-

Removed: 6.4.0

Default Value: false

Detail:
Allows [fast restart](https://aerospike.com/docs/database/manage/database/fast-start) for single bin, data in memory, integer or float data only pattern. For [single-bin](https://aerospike.com/docs/database/reference/config#namespace__single-bin) namespaces not configured with `data-in-index`, integer or float data will also be stored in the index but will not allow [fast restart](https://aerospike.com/docs/database/manage/database/fast-start) when [data-in-memory](https://aerospike.com/docs/database/reference/config#namespace__data-in-memory) is set to true.

---

#### `data-in-memory`

`static`

Context: namespace

Subcontext: storage-engine device

Description: Keep a copy of all data in memory always.

Introduced: \-

Removed: 7.0.0

Default Value: false

---

#### `data-size`

`required` `static`

Context: namespace

Subcontext: storage-engine memory

Description: Specifies the total amount of memory allocated for the in-memory (without storage-backed persistence) namespace’s eight virtual devices. This size is split into 8 stripes. The stripes appear individually in the logs. `data-size` is required, and only allowed, with `storage-engine` set to memory with no persistence to `device` or `file`. Each stripe uses the following overhead: \* 3 blocks for defragmentation \* 1 for master write-block (cwb) \* 1 for replica write-block \* 1 for migration write-block \* 1 for MRT write-block (in 8.0+) Consequently, the data size should be at least 512MiB (8 stripes \* 8 write-blocks \* 8MiB), preferably 1GiB or more.

-   Recommended: 1GiB.
-   Minimum: 512 MiB.
-   Maximum: 2 TiB.

Stop the `asd` service before modifying the `data-size` value. Clear the shared memory segments before starting `asd` again. For more information, see [How to change `data-size` configuration in a running cluster](https://support.aerospike.com/s/article/How-to-change-data-size-config-in-a-running-cluster).

Introduced: 7.0.0

Removed: \-

Default Value: \-

Detail:
Supports the following suffixes:

-   K Kibibyte (KiB)
-   M Mebibyte (MiB)
-   G Gibibyte (GiB)
-   T Tebibyte (TiB)

**Example:**

```asciidoc
data-size 500G
```

---

#### `default-read-touch-ttl-pct`

`dynamic` `cloud`

Context: namespace

Subcontext: set

Description: In the namespace configuration, a value of 0 disables the “read touch” feature, meaning read operations never extend a record’s TTL. Values from 1-100 represent a percentage of the record’s total lifespan; if a read occurs within this final percentage of time before expiration, the server automatically “touches” the record. This touch uses the record’s previous TTL to extend its life. For example, if a record has a 100-minute TTL and the threshold is set to 10, a read occurring during the last 10 minutes will reset the TTL back to 100 minutes. For the set configuration, 0 means use the namespace value. A set-level configuration can explicitly override the default namespace value: -1 means reads never touch a record. Values 1-100 are the same as the namespace configuration. Clients may also send a read-touch TTL percent: 0 instructs the server to use its configuration. Other values override the server configuration. -1 means reads never touch a record, values 1-100 are the same as the server configurations.

Introduced: 7.1.0

Removed: \-

Default Value: 0

Detail:
Queries, UDFs and writes which do not change records do not behave like reads for this feature. Starting with versions 7.1.0.19, 7.2.0.13, 8.0.0.11, and 8.1.0.2, read-touch operations do not advance the record generation counter, since only the TTL is being modified and not the record contents.

---

#### `default-ttl`

`dynamic` `cloud`

Context: namespace

Subcontext: set

Description: Default time to live for a record, from the time the record is created or last updated. The record expires in the system beyond this time. The default value is 0, specifying that records never expire. The maximum value is 3650D, or ten years.

Configuring `default-ttl` at the set level overrides any `default-ttl` configured at the namespace level.

Introduced: 7.0.0

Removed: \-

Default Value: 0

Detail:
Supports the following suffixes:

-   S Second
-   M Minute
-   H Hour
-   D Day

**Example:**

```ruby
namespace test {

  ...

  default-ttl 60D # use 0 to never expire/evict.

  ...

    set test-set {

      ...

      default-ttl 30D

      ...

    }

}
```

**Dynamically set `default-ttl` to 30 days:**

Terminal window

```bash
asinfo -v "set-config:context=namespace;namespace=namespaceName;set=test-set;default-ttl=30D"
```

Can be overridden using API.

As of Database 7.2.0, `id=` is deprecated in `set-config` and replaced with `namespace=`.

Reducing an existing record’s TTL (or issuing a non durable delete) may cause older versions of the records to be resurrected upon cold restarts. For more details, see [Why are deleted records resurrected after a cold start in AP mode?](https://support.aerospike.com/s/article/FAQ-Why-are-deleted-records-resurrected-after-a-cold-start-in-AP-mode)

---

#### `default-ttl`

`dynamic` `cloud`

Context: namespace

Description: Default time to live for a record, from the time the record is created or last updated. The record expires in the system beyond this time. The default value is 0, specifying that records never expire. The maximum value is 3650D, or ten years.

Introduced: \-

Removed: \-

Default Value: 0

Detail:
Supports the following suffixes:

-   S Second
-   M Minute
-   H Hour
-   D Day

**Example:**

```ruby
namespace test {

  ...

  default-ttl 60D # use 0 to never expire/evict.

  ...

}
```

**Dynamically set `default-ttl` to 30 days:**

Terminal window

```bash
asinfo -v "set-config:context=namespace;namespace=namespaceName;default-ttl=30D"
```

Can be overridden using API.

As of Database 7.2.0, `id=` is deprecated in `set-config` and replaced with `namespace=`.

Reducing an existing record’s TTL (or issuing a non durable delete) may cause older versions of the records to be resurrected upon cold restarts. For more details, see [Why are deleted records resurrected after a cold start in AP mode?](https://support.aerospike.com/s/article/FAQ-Why-are-deleted-records-resurrected-after-a-cold-start-in-AP-mode)

---

#### `defrag-lwm-pct`

`dynamic` `cloud`

Context: namespace

Subcontext: storage-engine device or storage-engine pmem or storage-engine memory

Description: Blocks that are less filled in percentage than the specified limit will be marked as eligible to be defragmented.

Also, wblocks that are in the [`post-write-queue`](https://aerospike.com/docs/database/reference/config#namespace__post-write-queue) (before Database 7.1.0) or [`post-write-cache`](https://aerospike.com/docs/database/reference/config#namespace__post-write-cache) (Database 7.1.0 and later) are not eligible to be defragmented. Therefore the `post-write-queue` should be kept small compared to the overall device size as the size allocated to the `post-write-queue` will not be defragmented.

Introduced: \-

Removed: \-

Default Value: 50

Detail:
**Example:** Set `defrag-lwm-pct` to 55:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;defrag-lwm-pct=55"
```

A higher percentage means more blocks to be defragmented and denser data on the disk.

Do **not** set the value to 100% or higher as it would put the system in an endless busy loop.

---

#### `defrag-queue-min`

`dynamic` `cloud`

Context: namespace

Subcontext: storage-engine device or storage-engine pmem or storage-engine memory

Description: Don’t defrag unless the queue has this many eligible wblocks.

Introduced: 3.4.0 7.0.0 (storage-engine memory)

Removed: \-

Default Value: 0

Detail:
**Example:** Set defrag-queue-min to 10:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;defrag-queue-min=10"
```

This may reduce write amplification for use cases with infrequent record overwrites or periodic record purges by allowing write blocks to linger on the queue longer and potentially be nearly empty when processed.

---

#### `defrag-sleep`

`dynamic` `cloud`

Context: namespace

Subcontext: storage-engine device or storage-engine pmem or storage-engine memory

Description: Number of microseconds to sleep after each wblock is defragmented. In Database 7.1.0 and later, this configuration controls the time to sleep between reading segments of size [`flush-size`](https://aerospike.com/docs/database/reference/config#namespace__flush-size).

Introduced: 3.3.17 7.0.0 (storage-engine memory)

Removed: \-

Default Value: 1000

Detail:
**Example:** Set defrag-sleep to 500:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;defrag-sleep=500"
```

A secondary usage of defrag-sleep is to define the interval at which the write queue is checked when defragmentation is throttled due to write queue overflow. Details on this can be found in [How does Aerospike defragmentation behave with respect to write queues?](https://support.aerospike.com/s/article/How-does-Aerospike-defragmentation-behave-with-respect-to-write-queues).

---

#### `defrag-startup-minimum`

`static` `cloud`

Context: namespace

Subcontext: storage-engine device or storage-engine pmem or storage-engine memory

Description: Server needs at least specified amount (in percentage) of free space at startup.

The value must be an integer and the allowable range is 0 to 99.

Prior to Database 5.7.0, the default value is 10 and the allowable range is 1 to 99.

Introduced: \-

Removed: \-

Default Value: 0

---

#### `device`

`static`

Context: namespace

Subcontext: storage-engine device or storage-engine memory

Description: Raw device used to store the namespace.

Introduced: \-

Removed: \-

Default Value: \-

Detail:
**Example:** Persist to two devices

```asciidoc
device /dev/sdb

device /dev/sdc
```

Persist to device and shadow device

```asciidoc
device /dev/nvme0n1 /dev/sdb
```

As of 4.3.0.2, when requesting the configuration using the ‘info’ API, the key for a particular device will be `storage-engine.device[ix]` where ‘ix’ is an index to identify this device with its associated statistics (such as the statistic [`storage-engine.device[ix].age`](https://aerospike.com/docs/database/reference/metrics#namespace__storage-engine.device%5Bix%5D.age)).

If configured, the device’s shadow device will appear as `storage-engine.device[ix].shadow`.

You can specify multiple devices per namespace per node.

The maximum limit on each device is 2 TiB.  
You may **not** use both **device** and **file** in the same namespace.  
The limit of 128 devices per namespace per node applies starting with Database 4.2.0 (64 for versions down to 3.12.1 and 32 in previous versions).

---

#### `direct-files`

`static` `cloud`

Context: namespace

Subcontext: storage-engine device or storage-engine pmem or storage-engine memory

Description: Relevant only for file storage. If using `storage-engine pmem`, relevant only for shadow file storage. If `direct-files` is set `true`, then the odirect and odsync flags are enabled for file IO. This means write-buffers are synchronously written all the way through to the devices under the file system. If using `storage-engine device` with [`data-in-memory`](https://aerospike.com/docs/database/reference/config#namespace__data-in-memory) set `false`, then it may be useful to set [`read-page-cache`](https://aerospike.com/docs/database/reference/config#namespace__read-page-cache) `true`. See the [Buffering and Caching in Aerospike](https://support.aerospike.com/s/article/Buffering-and-Caching-in-Aerospike) article for further details.

Introduced: 4.3.1 (device) 4.8.0 (pmem) 7.0.0 (storage-engine memory)

Removed: \-

Default Value: false

Detail:
Can impact performance, especially if files are backed by rotational devices.

---

#### `disable-cold-start-eviction`

`static` `cloud`

Context: namespace

Description: If `true`, disables eviction that may occur at cold start for this namespace only.

Introduced: 4.3.0.2

Removed: \-

Default Value: false

---

#### `disable-eviction`

`unanimous` `dynamic` `cloud`

Context: namespace

Subcontext: set

Description: `true` protects the set from evictions. Setting this parameter does not affect the TTL of records within the set. Records can have a TTL and will expire as normal.

This parameter is unanimous but not validated for unanimity across all nodes by the server. You must ensure that if you change it dynamically, all node configuration files are edited to ensure future restarts of any node stay unanimous for this parameter. If adding new nodes to the cluster, the configuration file must be correctly configured before the node joins the cluster to maintain unanimous configuration of this parameter.

Introduced: 5.6.0

Removed: \-

Default Value: false

Detail:
**Example:** Set disable-eviction on the set dynamically:

```asciidoc
Admin+> manage config namespace test set testset param disable-eviction to true"
```

Set disable-eviction under the namespace definition in aerospike.conf:

```plaintext
set set1 {

           disable-eviction true

  }

  set set2 {

           disable-eviction true

  }

  set test {

           disable-eviction true

  }
```

Eviction may happen at startup. It is good practice to enter protected sets into `aerospike.conf` as shown to prevent a protected set being evicted during cold start. This parameter was renamed from [`set-disable-eviction`](https://aerospike.com/docs/database/reference/config#namespace__set-disable-eviction) in Database 5.6.0.

---

#### `disable-mrt-writes`

`enterprise` `dynamic` `cloud`

Context: namespace

Description: Controls whether transactions can be used by applications. Blocks new transactions with writes by blocking monitor creates. Can be used dynamically to let an XDR destination settle to a transaction-consistent state.

Introduced: 8.0.0

Removed: \-

Default Value: false

---

#### `disable-odsync`

`static` `cloud`

Context: namespace

Subcontext: storage-engine device or storage-engine pmem or storage-engine memory

Description: If `disable-odsync` is set `true`, then the Linux O\_DSYNC I/O flag is set `false` (even if, for files, [`direct-files`](https://aerospike.com/docs/database/reference/config#namespace__direct-files) is set `true`). Disabling O\_DSYNC would likely improve performance at a cost of relaxed durability guarantees. See the [Buffering and Caching in Aerospike](https://support.aerospike.com/s/article/Buffering-and-Caching-in-Aerospike) article for further details.

Note: `disable-odsync` and [`commit-to-device`](https://aerospike.com/docs/database/reference/config#namespace__commit-to-device) cannot be both set to `true`. Setting both to true will prevent the server from starting given their opposition in the durability/performance trade off.

Introduced: 4.5.0.12, 4.5.1.8, 4.5.2.3, 4.5.3.3 7.0.0 (storage-engine memory)

Removed: \-

Default Value: false

Detail:
With data in PMem, this setting is only relevant for shadow file storage.  
  
Some further details on the effect of this setting: When a database record is written or updated, the changed record initially resides in a memory buffer on a server node in a structure known as the current write block. Write blocks are regularly flushed to SSD using Linux pwrite(2) syscalls, with the interval bounded by the [`flush-max-ms`](https://aerospike.com/docs/database/reference/config#namespace__flush-max-ms) configuration parameter. Until the a write block is persisted to SSD (by default at most 1 second after being written to DRAM), its contents are subject to loss in the event of a system failure (e.g. power outage). The default behavior (O\_DSYNC enabled) is that pwrite(2) will block the calling thread until the data has been written to the SSD. That delay reduces the work per unit of time a thread can do, potentially incurring a performance penalty. When O\_DSYNC is disabled a thread calling pwrite(2) will return immediately, enabling that thread to do other work. However the data may not be transferred to the device until some time in the future. If there is a system failure during the interval between calling pwrite(2) and when the data is completely written to SSD, there will be data loss (on that specific node only). Whether trading off durability against performance is worthwhile depends on the application, the Linux I/O implementation (which affects how quickly data is transferred), and the sensitivity of the record data. For some data (e.g. a frequently-updated sensor reading) the risk may be acceptable, for others (e.g. a financial transaction) it may not. A full description of Aerospike caching may be found [on this buffering and caching](https://support.aerospike.com/s/article/Buffering-and-Caching-in-Aerospike) knowledge base article.  
  
If you are utilizing the rack aware functionality for your cluster, the only way that we would expect a potential data loss is with Replication Factor (RF) number of servers failing within the SAME short duration, one second (at default) + virtual/cloud delay (if disable-odsync is turned on), as described above, one per rack, across the RF number of racks that store the copies of the record. So for example, in an RF=2 configuration with the servers split among two racks, for a potential loss of data to occur, a single server would have to fail in EACH rack within that very short duration.

---

#### `disable-write-dup-res`

`dynamic` `cloud`

Context: namespace

Description: Disables write duplicate resolution for the namespace. Only applicable for AP namespaces (non [strong-consistency](https://aerospike.com/docs/database/reference/config#namespace__strong-consistency) enabled). Write duplicate resolution is needed when recovering from node maintenance/failure or a partition. In such situations, a node will chase different versions of a record prior to applying the update. This only applies during migrations when multiple versions of a given partition may exist.

Introduced: 3.15.1.3

Removed: \-

Default Value: false

Detail:
Setting to true will disable write duplicate resolution which can improve write performance during migrations but may also result in lost updates.

---

#### `disallow-expunge`

`enterprise` `dynamic` `cloud`

Context: namespace

Description: For use with [available and partition-tolerant](https://aerospike.com/docs/database/learn/architecture/clustering/consistency-modes#ap-mode) (AP) namespaces only. When set to `true`, attempted [non-durable deletes](https://aerospike.com/docs/database/learn/architecture/durable-deletes) return [error code 22 (forbidden)](https://aerospike.com/docs/database/reference/error-codes).

Introduced: 6.3.0

Removed: \-

Default Value: false

---

#### `disallow-null-setname`

`dynamic` `cloud`

Context: namespace

Description: Enabling this configuration will error out a record write attempt if done without a set name.

Introduced: \-

Removed: \-

Default Value: false

Detail:
By default, Aerospike allows writes with and without a set name. If a record is sent without a setname, it gets assigned a ‘null’ set. If this configuration is enabled, any record without a setname will not be allowed to be written to the namespace. An ‘Error Code 4 AEROSPIKE\_ERR\_REQUEST\_INVALID’ will be sent back to the client. Additionally, a warning will be logged to the server with the message `null/empty set name not allowed for namespace`.

**Note**: Ensure that the configuration is set uniformly on all nodes. If that is not done, it would lead to situations when one node would allow such null-set records and others would not.

**Example:** Dynamically enabling this configuration:

```asciidoc
asinfo -v "set-config:context=namespace;id=namespaceName;disallow-null-setname=true"
```

---

#### `earth-radius-meters`

`static` `cloud`

Context: namespace

Subcontext: geo2dsphere-within

Description: Earth’s radius in meters, since the workspace here is the complete earth.

Introduced: 3.7.0.1

Removed: \-

Default Value: 6371000

---

#### `enable-benchmarks-batch-sub`

`dynamic` `cloud`

Context: namespace

Description: Enable histograms for batch sub transactions. See the [Histograms from Aerospike Logs](https://aerospike.com/docs/database/observe/latency) page for details.

Introduced: 3.9.0

Removed: \-

Default Value: false

Detail:
Here is the list of configuration enabled histograms:  

-   [`enable-benchmarks-batch-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-batch-sub)
-   [`enable-benchmarks-fabric`](https://aerospike.com/docs/database/reference/config#service__enable-benchmarks-fabric)
-   [`enable-benchmarks-ops-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-ops-sub)
-   [`enable-benchmarks-read`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-read)
-   [`enable-benchmarks-storage`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-storage)
-   [`enable-benchmarks-udf`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-udf)
-   [`enable-benchmarks-udf-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-udf-sub)
-   [`enable-benchmarks-write`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-write)
-   [`enable-hist-info`](https://aerospike.com/docs/database/reference/config#service__enable-hist-info)
-   [`enable-hist-proxy`](https://aerospike.com/docs/database/reference/config#namespace__enable-hist-proxy)
-   [`sindex-histogram`](https://aerospike.com/docs/database/observe/latency)

**Example:** Set `enable-benchmarks-batch-sub` to true:

```plaintext
asinfo -v 'set-config:context=namespace;id=<namespaceName>;enable-benchmarks-batch-sub=true'
```

---

#### `enable-benchmarks-ops-sub`

`dynamic` `cloud`

Context: namespace

Description: Enable histograms for ops sub transactions. See the [Histograms from Aerospike Logs](https://aerospike.com/docs/database/observe/latency) page for details.

Introduced: 4.7.0

Removed: \-

Default Value: false

Detail:
Here is the list of configuration enabled histograms:  

-   [`enable-benchmarks-batch-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-batch-sub)
-   [`enable-benchmarks-fabric`](https://aerospike.com/docs/database/reference/config#service__enable-benchmarks-fabric)
-   [`enable-benchmarks-ops-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-ops-sub)
-   [`enable-benchmarks-read`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-read)
-   [`enable-benchmarks-storage`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-storage)
-   [`enable-benchmarks-udf`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-udf)
-   [`enable-benchmarks-udf-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-udf-sub)
-   [`enable-benchmarks-write`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-write)
-   [`enable-hist-info`](https://aerospike.com/docs/database/reference/config#service__enable-hist-info)
-   [`enable-hist-proxy`](https://aerospike.com/docs/database/reference/config#namespace__enable-hist-proxy)
-   [`sindex-histogram`](https://aerospike.com/docs/database/observe/latency)

**Example:** Set `enable-benchmarks-ops-sub` to true:

```plaintext
asinfo -v 'set-config:context=namespace;id=<namespaceName>;enable-benchmarks-ops-sub=true'
```

---

#### `enable-benchmarks-read`

`dynamic` `cloud`

Context: namespace

Description: Enable histograms for read transactions. See the [Histograms from Aerospike Logs](https://aerospike.com/docs/database/observe/latency) page for details.

Introduced: 3.9.0

Removed: \-

Default Value: false

Detail:
Here is the list of configuration enabled histograms:  

-   [`enable-benchmarks-batch-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-batch-sub)
-   [`enable-benchmarks-fabric`](https://aerospike.com/docs/database/reference/config#service__enable-benchmarks-fabric)
-   [`enable-benchmarks-ops-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-ops-sub)
-   [`enable-benchmarks-read`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-read)
-   [`enable-benchmarks-storage`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-storage)
-   [`enable-benchmarks-udf`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-udf)
-   [`enable-benchmarks-udf-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-udf-sub)
-   [`enable-benchmarks-write`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-write)
-   [`enable-hist-info`](https://aerospike.com/docs/database/reference/config#service__enable-hist-info)
-   [`enable-hist-proxy`](https://aerospike.com/docs/database/reference/config#namespace__enable-hist-proxy)
-   [`sindex-histogram`](https://aerospike.com/docs/database/observe/latency)

**Example:** Set `enable-benchmarks-read` to true:

```plaintext
asinfo -v 'set-config:context=namespace;id=<namespaceName>;enable-benchmarks-read=true'
```

---

#### `enable-benchmarks-storage`

`dynamic` `cloud`

Context: namespace

Subcontext: storage-engine device or storage-engine pmem or storage-engine memory

Description: Enable histograms for storage access. See the [Histograms from Aerospike Logs](https://aerospike.com/docs/database/observe/latency) page for details.

Introduced: 3.9.0 (device) 4.8.0 (pmem) 7.0.0 (storage-engine memory)

Removed: \-

Default Value: false

Detail:
Here is the list of configuration enabled histograms:  

-   [`enable-benchmarks-batch-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-batch-sub)
-   [`enable-benchmarks-fabric`](https://aerospike.com/docs/database/reference/config#service__enable-benchmarks-fabric)
-   [`enable-benchmarks-ops-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-ops-sub)
-   [`enable-benchmarks-read`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-read)
-   [`enable-benchmarks-storage`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-storage)
-   [`enable-benchmarks-udf`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-udf)
-   [`enable-benchmarks-udf-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-udf-sub)
-   [`enable-benchmarks-write`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-write)
-   [`enable-hist-info`](https://aerospike.com/docs/database/reference/config#service__enable-hist-info)
-   [`enable-hist-proxy`](https://aerospike.com/docs/database/reference/config#namespace__enable-hist-proxy)
-   [`sindex-histogram`](https://aerospike.com/docs/database/observe/latency)

**Example:** Set `enable-benchmarks-storage` to true:

```plaintext
asinfo -v 'set-config:context=namespace;id=<namespaceName>;enable-benchmarks-storage=true'
```

---

#### `enable-benchmarks-udf-sub`

`dynamic` `cloud`

Context: namespace

Description: Enable histograms for udf sub transactions. See the [Histograms from Aerospike Logs](https://aerospike.com/docs/database/observe/latency) page for details.

Introduced: 3.9.0

Removed: \-

Default Value: false

Detail:
Here is the list of configuration enabled histograms:  

-   [`enable-benchmarks-batch-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-batch-sub)
-   [`enable-benchmarks-fabric`](https://aerospike.com/docs/database/reference/config#service__enable-benchmarks-fabric)
-   [`enable-benchmarks-ops-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-ops-sub)
-   [`enable-benchmarks-read`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-read)
-   [`enable-benchmarks-storage`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-storage)
-   [`enable-benchmarks-udf`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-udf)
-   [`enable-benchmarks-udf-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-udf-sub)
-   [`enable-benchmarks-write`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-write)
-   [`enable-hist-info`](https://aerospike.com/docs/database/reference/config#service__enable-hist-info)
-   [`enable-hist-proxy`](https://aerospike.com/docs/database/reference/config#namespace__enable-hist-proxy)
-   [`sindex-histogram`](https://aerospike.com/docs/database/observe/latency)

**Example:** Set `enable-benchmarks-udf-sub` to true:

```plaintext
asinfo -v 'set-config:context=namespace;id=<namespaceName>;enable-benchmarks-udf-sub=true'
```

---

#### `enable-benchmarks-udf`

`dynamic` `cloud`

Context: namespace

Description: Enable histograms for udf transactions. See the [Histograms from Aerospike Logs](https://aerospike.com/docs/database/observe/latency) page for details.

Introduced: 3.9.0

Removed: \-

Default Value: false

Detail:
Here is the list of configuration enabled histograms:  

-   [`enable-benchmarks-batch-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-batch-sub)
-   [`enable-benchmarks-fabric`](https://aerospike.com/docs/database/reference/config#service__enable-benchmarks-fabric)
-   [`enable-benchmarks-ops-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-ops-sub)
-   [`enable-benchmarks-read`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-read)
-   [`enable-benchmarks-storage`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-storage)
-   [`enable-benchmarks-udf`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-udf)
-   [`enable-benchmarks-udf-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-udf-sub)
-   [`enable-benchmarks-write`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-write)
-   [`enable-hist-info`](https://aerospike.com/docs/database/reference/config#service__enable-hist-info)
-   [`enable-hist-proxy`](https://aerospike.com/docs/database/reference/config#namespace__enable-hist-proxy)
-   [`sindex-histogram`](https://aerospike.com/docs/database/observe/latency)

**Example:** Set `enable-benchmarks-udf` to true:

```plaintext
asinfo -v 'set-config:context=namespace;id=<namespaceName>;enable-benchmarks-udf=true'
```

---

#### `enable-benchmarks-write`

`dynamic` `cloud`

Context: namespace

Description: Enable histograms for write transactions. See the [Histograms from Aerospike Logs](https://aerospike.com/docs/database/observe/latency) page for details.

Introduced: 3.9.0

Removed: \-

Default Value: false

Detail:
Here is the list of configuration enabled histograms:  

-   [`enable-benchmarks-batch-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-batch-sub)
-   [`enable-benchmarks-fabric`](https://aerospike.com/docs/database/reference/config#service__enable-benchmarks-fabric)
-   [`enable-benchmarks-ops-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-ops-sub)
-   [`enable-benchmarks-read`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-read)
-   [`enable-benchmarks-storage`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-storage)
-   [`enable-benchmarks-udf`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-udf)
-   [`enable-benchmarks-udf-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-udf-sub)
-   [`enable-benchmarks-write`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-write)
-   [`enable-hist-info`](https://aerospike.com/docs/database/reference/config#service__enable-hist-info)
-   [`enable-hist-proxy`](https://aerospike.com/docs/database/reference/config#namespace__enable-hist-proxy)
-   [`sindex-histogram`](https://aerospike.com/docs/database/observe/latency)

**Example:** Set `enable-benchmarks-write` to true:

```plaintext
asinfo -v 'set-config:context=namespace;id=<namespaceName>;enable-benchmarks-write=true'
```

---

#### `enable-hist-proxy`

`dynamic` `cloud`

Context: namespace

Description: Enable histograms for proxy transactions. See the [Histograms from Aerospike Logs](https://aerospike.com/docs/database/observe/latency) page for details.

Introduced: 3.9.0

Removed: \-

Default Value: false

Detail:
Here is the list of configuration enabled histograms:  

-   [`enable-benchmarks-batch-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-batch-sub)
-   [`enable-benchmarks-fabric`](https://aerospike.com/docs/database/reference/config#service__enable-benchmarks-fabric)
-   [`enable-benchmarks-ops-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-ops-sub)
-   [`enable-benchmarks-read`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-read)
-   [`enable-benchmarks-storage`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-storage)
-   [`enable-benchmarks-udf`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-udf)
-   [`enable-benchmarks-udf-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-udf-sub)
-   [`enable-benchmarks-write`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-write)
-   [`enable-hist-info`](https://aerospike.com/docs/database/reference/config#service__enable-hist-info)
-   [`enable-hist-proxy`](https://aerospike.com/docs/database/reference/config#namespace__enable-hist-proxy)
-   [`sindex-histogram`](https://aerospike.com/docs/database/observe/latency)

**Example:** Set `enable-hist-proxy` to true:

```plaintext
asinfo -v 'set-config:context=namespace;id=<namespaceName>;enable-hist-proxy=true'
```

---

#### `enable-index`

`dynamic` `cloud`

Context: namespace

Subcontext: set

Description: Setting this to `true` maintains an index specific to the set, which is used for scans of the set. Using such an index improves performance of scans of the set if the set is very small compared to the size of its namespace. See [Set Indexes](https://aerospike.com/docs/database/learn/architecture/data-storage/set-index) for further details.

Introduced: 5.6.0

Removed: \-

Default Value: false

Detail:
**Example:** Enable a set-specific index within the namespace definition in the configuration file:

```asciidoc
set setName {

           enable-index true

  }
```

Dynamically enable a set-specific index:

```asciidoc
asadm -e "enable; manage config namespace namespaceName set setName param enable-index to true"
```

To check the `enable-index` configuration for a specific set:

```asciidoc
Admin> show stat sets like enable

~~~~~~~~~~sandbox ufodata Set Statistics (2024-10-15 22:15:38 UTC)~~~~~~~~~~

Node        |jupyter-aerospike-2dexamp-2dctive-2dnotebooks-2duh4zco0l:3000

enable-index|false

Number of rows: 2
```

---

#### `enable-xdr`

`dynamic`

Context: namespace

Description: This controls, at the namespace level, whether digest log entries are being written to the digest log. This therefore practically controls whether records are being shipped through XDR globally, assuming DCs are configured and available, [xdr-shipping-enabled](https://aerospike.com/docs/database/reference/config#xdr__xdr-shipping-enabled) is kept at its default value (true) and the `enable-xdr` configuration is set to true at the XDR stanza level.  
Configured DCs that are linked to namespaces will be connected to independently of the value of this setting. To prevent the connections from being made, you will need to either a) [remove all seed nodes](https://aerospike.com/docs/database/reference/config#xdr__dc-node-address-port) from the datacenter definition, or b) [remove the datacenter](https://aerospike.com/docs/database/reference/config#namespace__xdr-remote-datacenter) from all namespace definitions, or do so dynamically to break existing connections.

Introduced: \-

Removed: 5.0.0

Default Value: false

Detail:
**Example:** Enable XDR dynamically on the namespace:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;enable-xdr=true"
```

---

#### `encryption-key-file`

`enterprise` `static`

Context: namespace

Subcontext: storage-engine device or storage-engine pmem or storage-engine memory

Description: Specifies a user-supplied encryption key and activates storage encryption. For more information see [Configuring Encryption at Rest](https://aerospike.com/docs/database/manage/security/encryption).  

This parameter’s value must follow one of these formats. Prefixes `file:`, `env:`, `env-b64:`, `vault:`, and `secrets:` are literal strings.

-   `file:/path/to/encryption-key-file` - Read from the filesystem (the `file:` prefix is optional).
-   `env-b64:ENCKEY` - Read from the named environment variable (Database 5.3.0+).
-   `vault:encryption-key` - the named secret will be read from [Vault](https://aerospike.com/docs/database/manage/security/vault) (Database 5.1.0+).
-   `secrets:AerospikeSecrets:EncryptionKey` - fetched using [Aerospike Secret Agent](https://aerospike.com/docs/database/manage/security/secrets) (Database 6.4.0+).

Introduced: 3.1.05.1 (device) 4.8.0 (pmem) 7.0.0 (storage-engine memory)

Removed: \-

Default Value: N/A

Detail:
**Example:** Enable encryption at rest for namespace _test_:

```plaintext
namespace test {

   ...

   storage-engine device {

      device /dev/sda1

      ...

      encryption-key-file /etc/aerospike/key.dat

   }

   ...

}
```

Enable encryption at rest for namespace _test_, with the encryption key secret fetched from HashiCorp Vault:

```asciidoc
namespace test {

   ...

   storage-engine device {

      device /dev/sda1

      ...

      encryption-key-file vault:encryption-key

   }

   ...

}
```

This is **not** the actual key used for encryption of the stored data. That key is generated by the system when data is first written to the storage and does not change unless the storage is completely wiped. The Aerospike encryption-key-file provides access to the actual key.

The contents of the encryption key is loaded at startup, just after parsing the configuration file. Once the Aerospike daemon (`asd`) is running, you may safely remove the key file. Store them safely! You will not be able to restart the Aerospike process without these files.

For increased security, the encryption key file may reside in a RAM-backed file system instead of a file system backed by physical storage media.

Prior to 5.7: Adding, removing or changing the key file requires stopping the Aerospike daemon, zeroizing the storage devices and restarting the Aerospike daemon. Migrations should complete prior to proceeding to the next node in the cluster. It is therefore possible to make such changes as a rolling fashion across a cluster.

---

#### `encryption-old-key-file`

`enterprise` `static`

Context: namespace

Subcontext: storage-engine device or storage-engine pmem or storage-engine memory

Description: Works together with the [`encryption-key-file`](https://aerospike.com/docs/database/reference/config#namespace__encryption-key-file) when rotating the storage encryption key. For more information see [Configuring Encryption at Rest](https://aerospike.com/docs/database/manage/security/encryption).  

This parameter’s value must follow one of these formats. Prefixes `file:`, `env:`, `env-b64:`, `vault:`, and `secrets:` are literal strings.

-   `file:/path/to/old-encryption-key-file` - Read from the filesystem (the `file:` prefix is optional).
-   `env-b64:OLDENCKEY` - Read from the named environment variable (Database 5.3.0+).
-   `vault:old-encryption-key` - the named secret will be read from [Vault](https://aerospike.com/docs/database/manage/security/vault) (Database 5.1.0+).
-   `secrets:AerospikeSecrets:OldEncryptionKey` - fetched using [Aerospike Secret Agent](https://aerospike.com/docs/database/manage/security/secrets) (Database 6.4.0+).

Introduced: 5.7.0 7.0.0 (storage-engine memory)

Removed: \-

Default Value: N/A

Detail:
**Example:** Rotate the encryption keys for namespace _test_:

```plaintext
namespace test {

   ...

   storage-engine device {

      device /dev/sda1

      ...

      encryption-key-file key.dat

      encryption-old-key-file /etc/aerospike/old-key.dat

   }

   ...

}
```

Fetch the encryption keys for namespace _test_ from HashiCorp Vault and rotate them:

```asciidoc
namespace test {

   ...

   storage-engine device {

      device /dev/sda1

      ...

      encryption-key-file vault:encryption-key

      encryption-old-key-file vault:old-encryption-key

   }

   ...

}
```

This is **not** the actual key used for encryption of the stored data. That key is generated by the system when data is first written to the storage and does not change unless the storage is completely wiped. The Aerospike encryption-key-file provides access to the actual key.

The contents of the user-supplied encryption key and the old encryption key are loaded at startup, just after parsing the configuration file. Once the Aerospike daemon is running, you may safely remove the encryption key files. Store them safely! You will not be able to restart the Aerospike process without these files.

Prior to 5.7: Adding, removing or changing the encryption key requires zeroizing the namespace storage devices.

---

#### `encryption`

`enterprise` `static` `cloud`

Context: namespace

Subcontext: storage-engine device or storage-engine pmem or storage-engine memory

Description: Specifies the algorithm used to generate the data encryption key - `aes-128` or `aes-256`.  
For more information see [Configuring Encryption at Rest](https://aerospike.com/docs/database/manage/security/encryption).

Introduced: 4.5.0 (device) 4.8.0 (pmem) 7.0.0 (storage-engine memory)

Removed: \-

Default Value: aes-128

---

#### `evict-hist-buckets`

`dynamic` `cloud`

Context: namespace

Description: Number of histogram buckets used for evictions. Must be between 100 and 10,000,000. Takes effect on the next eviction round.

Introduced: 3.8.0

Removed: \-

Default Value: 10000

Detail:
**Example:** Set evict-hist-buckets to 200000:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;evict-hist-buckets=200000"
```

Each bucket costs 4 bytes of memory, so 10 Million buckets means a 40MB histogram. Note that cold-start eviction is a special case, where the number of histogram buckets used is at least 100,000. That is, 100,000 buckets are used unless the current evict-hist-buckets setting is larger.

---

#### `evict-indexes-memory-pct`

`dynamic` `cloud`

Context: namespace

Description: Aerospike monitors the total amount of index memory in use. If configured nonzero, and [`indexes-memory-budget`](https://aerospike.com/docs/database/reference/config#namespace__indexes-memory-budget) is also configured nonzero, and the combined size of the RAM indexes exceeds the configured percentage of the budget, this begins [evicting records](https://aerospike.com/docs/database/manage/namespace/retention) from the namespace. Default is 0, which means no budget. Range is 0-100.

Introduced: 7.1.0

Removed: \-

Default Value: 0

---

#### `evict-mounts-pct`

`enterprise` `dynamic`

Context: namespace

Subcontext: index-type flash, sindex-type flash, index-type pmem, sindex-type pmem

Description: Data is evicted if the mount’s utilization is greater than this specified percentage (of [`mounts-budget`](https://aerospike.com/docs/database/reference/config#namespace__mounts-budget)).  
  
Setting this parameter to zero (which is the default) disables this threshold.

Introduced: 7.0.0

Removed: \-

Default Value: 0

Detail:
Renamed in Database 7.0.0 from [`mounts-high-water-pct`](https://aerospike.com/docs/database/reference/config#namespace__mounts-high-water-pct). For more information see [Namespace Data Retention Configuration](https://aerospike.com/docs/database/manage/namespace/retention).

---

#### `evict-sys-memory-pct`

`enterprise` `dynamic`

Context: namespace

Subcontext: namespace

Description: Aerospike monitors the total amount of system memory in use, including non-Aerospike memory usage. If the amount of system memory in use out of the total system memory becomes greater than the specified percentage, Aerospike begins [evicting records](https://aerospike.com/docs/database/manage/namespace/retention) from the namespace. Default is 0 which mean no eviction will be done.

When using `evict-sys-memory-pct`, as opposed to other eviction thresholds where data storage and index allocation grow gradually to reach the threshold, an external process can rapidly exceed the eviction threshold and cause records to be deleted unexpectedly.

Introduced: 7.0.0

Removed: 7.2.0

Default Value: 0

Detail:
**Example:** Designate a `evict-sys-memory-pct` value within a namespace definition in the configuration file:

```asciidoc
evict-sys-memory-pct 75
```

Dynamically enable a `evict-sys-memory-pct` value:

```asciidoc
asinfo -v "set-config:context=namespace;id=namespaceName;evict-sys-memory-pct=75"
```

---

#### `evict-tenths-pct`

`dynamic` `cloud`

Context: namespace

Description: Maximum 1/10th percentage of objects to be deleted during each iteration of eviction.

Introduced: \-

Removed: \-

Default Value: 5

Detail:
**Example:** Set evict-tenths-pct to 10:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;evict-tenths-pct=10"
```

---

#### `evict-used-pct`

`dynamic` `cloud`

Context: namespace

Subcontext: storage-engine device or storage-engine pmem or storage-engine memory

Description: Data is evicted if the storage utilization is greater than this specified percentage.

Setting this parameter to zero disables this threshold.

Introduced: 7.0.0

Removed: \-

Default Value: 0

Detail:
**Example:** Set `evict-used-pct` to 60 using `asadm`:

```plaintext
Admin+> manage config namespace NAMESPACE_NAME storage-engine param evict-used-pct to 60
```

This example uses `asadm` to change the value for the entire cluster. The `asinfo` CLI tool only sends commands to one node at a time.

Records with TTL 0 will not be evicted. Data that is set to expire first, by TTL bucket, is first to be evicted.

For more information, see [Namespace data retention configuration](https://aerospike.com/docs/database/manage/namespace/retention).

---

#### `file`

`static`

Context: namespace

Subcontext: storage-engine device or storage-engine pmem or storage-engine memory

Description: Data file path on rotational disk (using a file system) or pmem (starting with Database 4.8). As of 4.3.0.2, the file may include an optional ‘shadow file’ as a second argument.

Introduced: \-

Removed: \-

Default Value: \-

Detail:
**Example:** Persist to two files:

```asciidoc
file /mnt/disk1/myfile1.dat

file /mnt/disk2/myfile2.dat
```

Persist to two files (pmem):

```asciidoc
file /mnt/pmem/myfile1.dat

file /mnt/pmem/myfile2.dat
```

Persist file with a shadow file:

```asciidoc
file /mnt/pmem1/rw_file.dat /mnt/sdb1/shadow_file.dat
```

```asciidoc
file /mnt/nvme0n1/rw_file.dat /mnt/sdb1/shadow_file.dat
```

As of 4.3.0.2, when requesting the configuration using the ‘info’ API, the key for a particular device will be ‘storage-engine.file\[ix\]’ where ‘ix’ is an index to identify this file with its associated statistics (such as the statistic ‘storage-engine.file\[ix\].age’).

If configured, the file’s shadow file will appear as ‘storage-engine.file\[ix\].shadow.

You can specify multiple files per namespace. The directory path should exist and the user/group the Aerospike process is running under should have read/write permissions. The file itself will be created by the process.

There is a maximum file size limit of 2 TiB.  
You must not use both `device` and `file` in the same namespace.  
There is a limit of 128 files per namespace starting with Database 4.2.0 (64 for versions down to 3.12.1 and 32 in previous versions).

---

#### `filesize`

`required` `static`

Context: namespace

Subcontext: storage-engine device or storage-engine pmem or storage-engine memory

Description: Maximum size for each `file` storage defined in this namespace. File header is 8M. Filesize must be a multiple of 8M and greater than 8M or server will not start. Maximum limit of 2 TiB on the `filesize`.

`filesize` is required to be set explicitly when the namespace is configured to use files.

Introduced: \-

Removed: \-

Default Value: \-

Detail:
Supports the following suffixes:

-   K Kibibyte (KiB)
-   M Mebibyte (MiB)
-   G Gibibyte (GiB)
-   T Tebibyte (TiB)

**Example:**

```asciidoc
filesize 500G
```

---

#### `flush-max-ms`

`dynamic` `cloud`

Context: namespace

Subcontext: storage-engine device or storage-engine pmem or storage-engine memory

Description: Configures the maximum amount of time that a Streaming Write Buffer (SWB) can go without being written to device or pmem storage file. This only becomes relevant for very low or intermittent write rates, since write buffers do get written to device (or pmem) when full. In general, changing this should not be necessary. Minimum 0: Don’t do partial flush. Maximum: No limit. See the [Buffering and Caching in Aerospike](https://support.aerospike.com/s/article/Buffering-and-Caching-in-Aerospike) article for further details.

Introduced: 3.3.21 (device) 4.8.0 (pmem) 7.0.0 (storage-engine memory)

Removed: \-

Default Value: 1000

Detail:
**Example:** Set flush-max-ms to 500:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;flush-max-ms=500"
```

Cannot be configured for an in-memory namespace without storage-backed persistence.

---

#### `flush-size`

`dynamic` `cloud`

Context: namespace

Subcontext: storage-engine device and storage-engine memory

Description: Specifies the size of write units for streaming write buffer (SWB) flushes. Must be a power of 2, from 4KiB to 8MiB (The configuration accepts the following values: 4K, 8K, 16K, 32K, 64K, 128K, 256K, 512K, 1M, 2M, 4M, 8M). The `flush-size` can be configured to match the [`write-block-size`](https://aerospike.com/docs/database/reference/config#namespace__write-block-size) used prior to Database 7.1.0. For most SSDs the ideal value may be 128KiB. Can be modified dynamically up or down.

Governs both partial writes and full writes, and can completely solve the problem of excess device I/O in workloads dominated by partial writes. For such workloads, configure `flush-size` to be relatively small, 128KiB or even less.

Introduced: 7.1.0

Removed: \-

Default Value: 1MiB

---

#### `high-water-disk-pct`

`dynamic`

Context: namespace

Description: Data is evicted if the disk utilization is greater than this specified percentage.  
  
Setting this parameter to zero (which is the default) disables this threshold.

Introduced: \-

Removed: 7

Default Value: 0

Detail:
**Example:** Set `high-water-disk-pct` to 60:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;high-water-disk-pct=60"
```

Records with TTL 0 are not evicted. Data set to expire first, by TTL bucket, is first to be evicted.  
  
See [Namespace Data Retention Configuration](https://aerospike.com/docs/database/manage/namespace/retention) for more information.  
  
Prior to Database 4.9.0, the default was 50.

Setting this parameter to 0 in releases earlier than Database 4.9.0 is not supported and may trigger immediate evictions.

Renamed in Database 7.0.0 to [`evict-used-pct`](https://aerospike.com/docs/database/reference/config#namespace__evict-used-pct).

---

#### `high-water-memory-pct`

`dynamic`

Context: namespace

Description: Data will be evicted if the memory utilization is greater than this specified percentage.  
  
Setting this parameter to zero (which is the default) disables this threshold.

Introduced: \-

Removed: 7.0.0

Default Value: 0

Detail:
**Example:** Set high-water-memory-pct to 60:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;high-water-memory-pct=60"
```

Records with TTL 0 are not evicted. Data set to expire first by TTL bucket is first to be evicted.  
  
For more information, see [Namespace Data Retention Configuration](https://aerospike.com/docs/database/manage/namespace/retention).  
  
Prior to Database 4.9.0, the default was 60.

Setting this parameter to 0 in releases earlier than Database 4.9.0 is not supported and may trigger immediate evictions.

---

#### `ignore-migrate-fill-delay`

`enterprise` `dynamic` `cloud`

Context: namespace

Description: Disables the [`migrate-fill-delay`](https://aerospike.com/docs/database/reference/config#service__migrate-fill-delay), which otherwise introduces a time lag before “fill” migrations occur to nodes that do not usually serve as replicas. This immediate repopulation behavior is important for non-persistent memory namespaces ([`storage-engine memory`](https://aerospike.com/docs/database/reference/config#namespace__storage-engine)), where there may be no disk-based data to restore after a restart and migrations are the only way to recover the dataset on a node. However, the configuration is valid and may be beneficial for any storage-engine type, depending on your recovery and performance requirements. Note that [`ignore-migrate-fill-delay`](https://aerospike.com/docs/database/reference/config#namespace__ignore-migrate-fill-delay) is not useful for [`strong-consistency`\-enabled](https://aerospike.com/docs/database/reference/config#namespace__strong-consistency) namespaces—even if they use non-persistent storage—because the roster controls partition ownership in those cases (rather than nodes present in the cluster).  
  
For more information, see [Delaying “Fill” Migrations](https://aerospike.com/docs/database/manage/cluster/delay-migrations).

Introduced: 5.2.0

Removed: \-

Default Value: false

Detail:
**Example:** To disregard the [`migrate-fill-delay`](https://aerospike.com/docs/database/reference/config#service__migrate-fill-delay) setting and cause `nameSpaceName` to begin “fill” migration: `asinfo -v "set-config:context=namespace;id=nameSpaceName;ignore-migrate-fill-delay=true"`.

---

#### `index-stage-size`

`static` `cloud`

Context: namespace

Description: Size of the primary index arena stages.

Introduced: 4.2.0.2

Removed: \-

Default Value: 1G

Detail:
This value must be a power of 2, and the permitted range of values for Community Edition (CE) and Enterprise Edition (EE) are as follows:

-   CE: Between 2^27 (128M) and 2^30 (1G)
-   EE: Between 2^27 (128M) and 2^34 (16G)

This value determines the size of each of the 256 (CE) or 2048 (EE) maximum possible arena stages for the primary index. Changing this value necessitates a coldstart.

Each arena is allocated incrementally and lazily, meaning that memory is allocated only as needed, in chunks of `index-stage-size`.

**Function and Impact**

The primary index is structured into a maximum of 2048 arenas per namespace, per node, and each record in the index consumes 64 bytes. Therefore, the maximum number of records a namespace can support per node is a function of `index-stage-size` and the fixed 2048 arena limit.

**Considerations**

-   Underprovisioning risk: If `index-stage-size` is set too low relative to the expected record count and available shared memory, the node may fail when trying to allocate the 2049th arena.
-   Overprovisioning impact: Setting this value too high, especially in environments with low record count, can lead to:
    -   Unused shared memory wastage or even out of memory errors.
    -   Longer runtime for [asmt](https://aerospike.com/docs/database/tools/asmt/), as each arena is fully backed up, regardless of record count.

**Recommendations**

-   Tune `index-stage-size` based on your expected record volume and available system shared memory.
-   Monitor memory usage during initial deployment to verify actual stage allocations.
-   Avoid using the maximum setting unless required by very large datasets.

The following table provides the maximum number of records for a namespace on a single node for Enterprise Edition:

| `index-stage-size` | Max records per namespace, per node |
| --- | --- |
| 128 MiB (minimum) | 4,294,967,296 |
| 1 GiB (default) | 34,359,738,368 |
| 16 GiB (maximum) | 549,755,813,888 |

Supported size notation is no-suffix for bytes, K for Kibibyte (KiB), M for Mebibyte (MiB), G for Gibibyte (GiB), T for Tebibyte (TiB), P for Pebibyte (PiB).

---

#### `index-type`

`enterprise` `static`

Context: namespace

Description: Options: pmem, shmem, flash

If `pmem`, the primary index is stored in persistent memory (e.g., Intel Optane DC Persistent Memory). If `shmem`, the primary index is stored in Linux shared memory. If `flash`, the primary index is stored in a block storage device (typically NVMe SSD). For information about `shmem` and `flash`, see [Configuring the primary index](https://aerospike.com/docs/database/manage/namespace/primary-index).

In all three options, the node is able to [fast-restart](https://aerospike.com/docs/database/manage/database/fast-start). If `pmem` or `flash` the primary index is also preserved across reboots of the node’s OS, allowing for fast-restart after the host machine reboots.

Setting to `flash` requires the `asdb-flash-index` feature-key, `pmem` requires the `asdb-pmem` feature-key to be enabled in the [`feature-key-file`](https://aerospike.com/docs/database/reference/config#service__feature-key-file).

In Database 7.0.0, `flash` does not work with `storage-engine pmem` or `storage-engine memory`.

Introduced: 4.3.0.2 (shmem) 4.3.0.2 (flash) 4.5.0.1 (pmem)

Removed: \-

Default Value: shmem

Detail:
On Community Edition, this will appear as ‘undefined’ and is not configurable.

---

#### `indexes-memory-budget`

`dynamic` `cloud`

Context: namespace

Description: Maximum amount of total memory for the indexes on this namespace, in bytes. If configured nonzero, and in conjunction with [`evict-indexes-memory-pct`](https://aerospike.com/docs/database/reference/config#namespace__evict-indexes-memory-pct), it will trigger stop-writes if the combined size of the RAM indexes (primary, secondary, and set indexes) exceeds the budget.

Introduced: 7.1.0

Removed: \-

Default Value: 0

Detail:
Supports the following suffixes:

-   K Kibibyte (KiB)
-   M Mebibyte (MiB)
-   G Gibibyte (GiB)
-   T Tebibyte (TiB)

**Example:**

```asciidoc
indexes-memory-budget 100G
```

---

#### `inline-short-queries`

`dynamic` `cloud`

Context: namespace

Description: In Database 6.3.0 and later, you have the option to run short queries inline, which means that one service thread executes the query, bypassing the query monitor. Ensure that queries designated as short queries return a small number of records, otherwise they might time out. This configuration is useful in cases where short query latency is a priority, and you are willing to potentially sacrifice some single-record transaction latency, as the service threads will be used for both.

See [Query features and short and long queries](https://aerospike.com/docs/develop/learn/queries) for more information.

Introduced: 6.3.0

Removed: \-

Default Value: false

---

#### `level-mod`

`static` `cloud`

Context: namespace

Subcontext: geo2dsphere-within

Description: If specified, then only cells where (level - min-level) is a multiple of “level-mod” will be used (default 1). This effectively allows the branching factor of the S2 Cell Id hierarchy to be increased. Currently the only parameter values allowed are 1, 2, or 3, corresponding to branching factors of 4, 16, and 64 respectively.

Introduced: 3.7.0.1

Removed: \-

Default Value: 1

---

#### `max-cells`

`dynamic` `cloud`

Context: namespace

Subcontext: geo2dsphere-within

Description: Sets the maximum desired number of cells in the approximation. The maximum number of cells allowed is 256.

Introduced: 3.7.0.1

Removed: \-

Default Value: 12

Detail:
**Example:** Changing max-cells dynamically:

```plaintext
asinfo -v "set-config:context=namespace;id=namespacename;geo2dsphere-within-max-cells=24"
```

-   Prior to Database 4.4.0, maximum allowed value is 32.

---

#### `max-level`

`dynamic` `cloud`

Context: namespace

Subcontext: geo2dsphere-within

Description: Maximum depth (number of subdivisions) to use for a single cell. This defines the minimum cell size to be used.

The allowable range for this parameter is 0 to 30. At level 20 the cell size varies from 46.4 to 97.3 square meters.

Introduced: 3.7.0.1

Removed: \-

Default Value: 20

Detail:
**Example:** Changing max-level dynamically:

```plaintext
asinfo -v "set-config:context=namespace;id=namespacename;geo2dsphere-within-max-level=25"
```

Cannot be set dynamically prior to Database 4.4.0.

Prior to Database 5.7.0, the default value is 30.

---

#### `max-record-size`

`dynamic` `cloud`

Context: namespace

Description: Specifies the maximum allowed record size in bytes up to 8MiB. The default is 1MiB. Any write attempt that breaches `max-record-size` fails with a [code 13](https://aerospike.com/docs/database/reference/error-codes) error, [`fail_record_too_big`](https://aerospike.com/docs/database/reference/metrics#namespace__fail_record_too_big).

Introduced: 5.7.0

Removed: \-

Default Value: 1M

Detail:
Supported size notation is no suffix for bytes, K for Kibibyte (KiB), M for Mebibyte (MiB).

**Example:** Changing max-record-size dynamically:

```plaintext
asinfo -v "set-config:context=namespace;id=ns1;max-record-size=256K"
```

In `asadm` the equivalent is:

Terminal window

```bash
Admin> enable

Admin+> manage config namespace ns1 param max-record-size to 256K
```

-   Prior to 7.1, the default is 0.

---

#### `max-used-pct`

`dynamic`

Context: namespace

Subcontext: storage-engine device or pmem

Description: Disallow writes except deletes, replica writes and migration writes, when the ratio of [`device_used_bytes`](https://aerospike.com/docs/database/reference/metrics#namespace__device_used_bytes) to [`device_total_bytes`](https://aerospike.com/docs/database/reference/metrics#namespace__device_total_bytes) (with storage-engine device) or the ratio of [`pmem_used_bytes`](https://aerospike.com/docs/database/reference/metrics#namespace__pmem_used_bytes) to [`pmem_total_bytes`](https://aerospike.com/docs/database/reference/metrics#namespace__pmem_total_bytes) (with storage-engine pmem) for the namespace is greater than this specified percentage. Writes are disallowed when the memory utilization for the namespace reached the configured [`stop-writes-pct`](https://aerospike.com/docs/database/reference/config#namespace__stop-writes-pct) or when the node’s system memory utilization reached the configured [`stop-writes-sys-memory-pct`](https://aerospike.com/docs/database/reference/config#namespace__stop-writes-sys-memory-pct).

Introduced: 6.3.0

Removed: 7.0.0

Default Value: 70

Detail:
**Example:** Designate a `max-used-pct` value within a namespace definition in the configuration file:

```asciidoc
max-used-pct 90
```

Dynamically enable a `max-used-pct` value:

```asciidoc
asinfo -v "set-config:context=namespace;id=namespaceName;max-used-pct=90"
```

Renamed in Database 7.0.0 to[`stop-writes-used-pct`](https://aerospike.com/docs/database/reference/config#namespace__stop-writes-used-pct).

---

#### `max-write-cache`

`dynamic` `cloud`

Context: namespace

Subcontext: storage-engine device or storage-engine pmem or storage-engine memory

Description: Number of bytes of pending write blocks that the system is allowed to keep before failing writes. The write cache implements a circuit-breaker to throttle excessive writes. Should be multiple of [`write-block-size`](https://aerospike.com/docs/database/reference/config#namespace__write-block-size). While `max-write-cache` has no maximum permitted value, the minimum value is 64M which is the default.

Introduced: 4.8.0 (pmem) 7.0.0 (storage-engine memory)

Removed: \-

Default Value: 64M

Detail:
The size of the write cache is calculated using the number of devices in the namespace multiplied by the value of `max-write-cache`. Client writes are allowed until the sum of all in-use streaming write buffers (SWB) equals the calculated amount. To see how many streaming write buffers are in use, look at the [write\_q](https://aerospike.com/docs/database/reference/metrics#namespace__storage-engine.device%5Bix%5D.write_q) stat (or [shadow\_write\_q](https://aerospike.com/docs/database/reference/metrics#namespace__storage-engine.device%5Bix%5D.shadow_write_q)) or directly at the `write-q` on the [defrag log line](https://aerospike.com/docs/database/reference/logs).

**Example - How write cache is calculated**

The write cache size is the number of devices for the namespace on the node, multiplied by the value of `max-write-cache`. The cache for each device must be accounted for in the total sizing calculation.

Each device has its own write queue (write-q). Assume the following:

-   a 3-node cluster with 1 namespace and 4 devices for that namespace on each node (12 total across the cluster)
-   `max-write-cache` is set at the default 64MiB and the write-blocks are always 8MiB. When the sum of all pending blocks across the 4 write queues breaches 256MiB (64MiB x 4), the `write fail: queue too deep:` error and **[Error Code 18: Device overload](https://aerospike.com/docs/database/reference/error-codes)** are thrown.

The write cache does not have to be the same size on each of the 4 devices in this example. Each could have 64MiB (or 8 blocks) or 1 of could have 256MiB (or 32 blocks) and the other three are keeping up and are at 0.

If you configure `max-write-cache` to 128MiB and have 10 devices on the namespace on each node, you need to account for potentially using up 128MiB x 10 = 1280MiB of RAM in case you go all the way to that value.

**Tip:** When the queue grows beyond the configured limit and device overload errors appear you can dynamically increase the `max-write-cache` limit with the following example command.

```plaintext
asinfo -v 'set-config:context=namespace;id=namespaceName;max-write-cache=128M'
```

For more details, see the [Log Reference](https://aerospike.com/docs/database/reference/logs) and [Resilience](https://aerospike.com/docs/database/learn/architecture/data-storage/resilience).

---

#### `memory-size`

`required` `dynamic`

Context: namespace

Description: Starting with Database 7.0.0, a namespace that stores its data in memory, pre-allocates the memory used for data storage, so the indexes are the main consumers of unallocated memory. In this case, replace `memory-size` with [`indexes-memory-budget`](https://aerospike.com/docs/database/reference/config#namespace__indexes-memory-budget), which declares the maximum amount of memory that the namespace can use for all indexes combined (primary, secondary and set indexes).

In versions prior to Database 7.0.0, `memory-size` controls the amount of memory used by the namespace, including the indexes and any data in stored memory. Cannot be reduced by more than 50% of previously set value. See [Capacity Planning](https://aerospike.com/docs/database/manage/planning/capacity) for namespace sizing details.

Prior to 4.3.0.2, the default value was 4GiB. As of 4.3.0.2, `memory-size` is required to be explicitly configured, with a minimum of 1MiB.

Introduced: \-

Removed: 7.0.0

Default Value: \-

Detail:
Supported size notation is no suffix for bytes, K for Kibibyte (KiB), M for Mebibyte (MiB), G for Gibibyte (GiB), T for Tebibyte (TiB).

**Example:**

```asciidoc
memory-size 10G
```

Set memory-size to 12G dynamically:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;memory-size=12G"
```

This is not a hard limit. A namespace’s used memory could go above this threshold under some specific situations. The `memory-size` value is mainly used to infer the [`high-water-memory-pct`](https://aerospike.com/docs/database/reference/config#namespace__high-water-memory-pct) and [`stop-writes-pct`](https://aerospike.com/docs/database/reference/config#namespace__stop-writes-pct). This should be set accordingly to the total available memory on the instance (leaving enough for the OS) and the memory allocated to other namespaces. An empty and unused namespace would still allocate 1GiB of shared memory (Enterprise Edition).

---

#### `migrate-order`

`dynamic` `cloud`

Context: namespace

Description: Number between 1 and 10 which determines the order namespaces are to be processed when migrating. Namespaces are processed in ascending order (lowest to highest) according to this configuration.

Introduced: 3.7.5

Removed: \-

Default Value: 5

Detail:
**Example:** Set migrate-order to 1:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;migrate-order=1"
```

A namespace with a higher `migrate-order` may still make some progress before namespaces with lower `migrate-order` have completed. Here is an explanation for this behavior:  
Migration happen in units of partition.  
A partition is ready to migrate out (emigrate) if:  
a. the node is a replica and the partition needs to be send to the master for merging.  
b. the node is a master for the partition and has received and merged all different versions of the partition from the replica.  
  
So on a node, even if a namespace has a lower `migrate-order`, if it is master for a partition, it will have to wait for replicas to send it their copies of this partition before it can emigrate the merged partition back to the replicas. To maintain strict `migrate-order` the node will have to just wait and do nothing. However to speed up the entire migration process, we choose to allow this node to emigrate higher `migrate-order` namespace partitions if they are ready.

---

#### `migrate-retransmit-ms`

`dynamic` `cloud`

Context: namespace

Description: How long to wait for success, in milliseconds, before retrying a migration related transaction. In Database 3.1.00.1, even though `migrate-retransmit-ms` is honored and set to 5000ms, it cannot be retrieved through the info protocol and cannot be set.

Introduced: 3.1.01.0

Removed: \-

Default Value: 5000

Detail:
**Example:** Set migrate-retransmit-ms to 2500:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;migrate-retransmit-ms=2500"
```

---

#### `migrate-skip-unreadable`

`static` `cloud`

Context: namespace

Description: If `true`, skips writing a record locally during a migration if the record fails validation.

Use this setting only in consultation with Aerospike Support, and only if you are experiencing persistent issues with drive firmware or hardware. Work with your firmware or drive manufacturer to resolve any data integrity issues.

Skipped record count available in [`migrate_records_unreadable`](https://aerospike.com/docs/database/reference/metrics#namespace__migrate_records_unreadable).

Introduced: 7.0.0.18, 7.1.0.9, 7.2.0.3

Removed: \-

Default Value: false

---

#### `migrate-sleep`

`dynamic`

Context: namespace

Description: Number of microseconds to sleep after each record migration. This parameter can be decreased to 0 in order to speed up migrations. See [manage migrations](https://aerospike.com/docs/database/manage/cluster/migrations#speeding-up-the-migration-rate) for further details.

Introduced: 3.7.5

Removed: \-

Default Value: 1

Detail:
**Example:** Set migrate-sleep to 0:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;migrate-sleep=0"
```

Does not impact the metadata comparison part of the migration process. Only affects the time to sleep between sending actual records.

---

#### `min-avail-pct`

`dynamic`

Context: namespace

Subcontext: storage-engine device or pmem

Description: Disallow writes except deletes, replica writes and migration writes when [`device_available_pct`](https://aerospike.com/docs/database/reference/metrics#namespace__device_available_pct) on one of the devices or pmem files configured for the namespace is below this specified percentage.

Introduced: 3.1.10 (device) 4.8.0 (pmem)

Removed: 7.0.0

Default Value: 5

Detail:
Writes are disallowed when memory utilization for the namespace reaches the configured [`mounts-high-water-pct`](https://aerospike.com/docs/database/reference/config#namespace__mounts-high-water-pct).

Renamed in Database 7.0.0 to [`stop-writes-avail-pct`](https://aerospike.com/docs/database/reference/config#namespace__stop-writes-avail-pct).

We do not recommend setting this value below 5%. Doing so may not allow enough buffer room for replica writes and migrations writes. This may lead to not having enough free blocks for defrag to recover the system, in which case the node would need to cold start to recover.

---

#### `min-level`

`dynamic` `cloud`

Context: namespace

Subcontext: geo2dsphere-within

Description: Minimum depth (number of subdivisions) to use for a single cell. This defines the maximum cell size to be used.

The allowable range for this parameter is 0 to 30. At level 1 the cell size is 21,252,753 square kilometers.

Introduced: 3.7.0.1

Removed: \-

Default Value: 1

Detail:
**Example:** Changing min-level dynamically:

```plaintext
asinfo -v "set-config:context=namespace;id=namespacename;geo2dsphere-within-min-level=5"
```

Cannot be set dynamically prior to Database 4.4.0.

---

#### `mount`

`enterprise` `static`

Context: namespace

Subcontext: index-type flash, sindex-type flash, index-type pmem, sindex-type pmem

Description: Path to the mount directory, typically on NVMe SSD. There may be more than one mount per namespace: in Database 7.0.0 maximum is 32, pre-7.0 maximum is 16. Although not recommended, a mount may be shared with other namespaces. For sizing details when using [`index-type flash`](https://aerospike.com/docs/database/reference/config#namespace__index-type), see the [Capacity Planning](https://aerospike.com/docs/database/manage/planning/capacity/#primary-index-on-flash) page.

When using [`index-type pmem`](https://aerospike.com/docs/database/reference/config#namespace__index-type) or [`sindex-type pmem`](https://aerospike.com/docs/database/reference/config#namespace__sindex-type) with [`auto-pin numa`](https://aerospike.com/docs/database/reference/config#service__auto-pin), configured mounts that are not on the local NUMA node are ignored. Therefore, different instances of Aerospike server running on different NUMA nodes may share the same configured mounts without the operator needing to determine which mounts are on which NUMA nodes.

Introduced: 4.3.0.2 (flash), 4.5.0.1 (pmem), 6.3.0 (sindex-type pmem)

Removed: \-

Default Value: \-

Detail:
When requesting the configuration using the ‘info’ API, the key for a particular mount will be `storage-engine.mount[ix]` where ‘ix’ is an index to identify this mount with its associated statistics (such as the statistic [`index-type.mount[ix].age`](https://aerospike.com/docs/database/reference/metrics#namespace__index-type.mount%5Bix%5D.age)).

---

#### `mounts-budget`

`enterprise` `required` `dynamic`

Context: namespace

Subcontext: index-type flash, sindex-type flash, index-type pmem, sindex-type pmem

Description: Maximum amount of total device space for the mount(s) on this namespace. For example, if there are two mount points of 100GiB each, then `mounts-budget` should be set to 200GiB. The minimum size is 1GiB and maximum is to not exceed to the total capacity of all the mount point\[s\]. This does not prevent sprigs from being allocated beyond the limit, but rather enforces the eviction of records based on the [`evict-mounts-pct`](https://aerospike.com/docs/database/reference/config#namespace__evict-mounts-pct) configuration which is measured against the index usage (based on the number of records rather than the number of sprigs). See [All Flash capacity sizing](https://aerospike.com/docs/database/manage/planning/capacity/#primary-index-on-flash) for further details.

Required to be explicitly set when using [`index-type flash`](https://aerospike.com/docs/database/reference/config#namespace__index-type) or [`index-type pmem`](https://aerospike.com/docs/database/reference/config#namespace__index-type).

Introduced: 7.0.0

Removed: \-

Default Value: \-

Detail:
Supported size notation is no suffix for bytes, K for Kibibyte (KiB), M for Mebibyte (MiB), G for Gibibyte (GiB), T for Tebibyte (TiB), P for Pebibyte (PiB).

Renamed in Database 7.0.0 from [`mounts-size-limit`](https://aerospike.com/docs/database/reference/config#namespace__mounts-size-limit)

---

#### `mounts-high-water-pct`

`enterprise` `dynamic`

Context: namespace

Subcontext: index-type flash, sindex-type flash, index-type pmem, sindex-type pmem

Description: Data is evicted if the mount’s utilization is greater than this specified percentage (of [`mounts-size-limit`](https://aerospike.com/docs/database/reference/config#namespace__mounts-size-limit)).  
  
Setting this parameter to zero (the default) disables this threshold.

Introduced: 4.3.0.2 (flash) 4.5.0.1 (pmem), 6.3.0 (sindex-type pmem)

Removed: 7.0.0

Default Value: 0

Detail:
For more information see [Namespace Data Retention Configuration](https://aerospike.com/docs/database/manage/namespace/retention).  
  
Prior to Database 4.9.0, the default was 80.

Setting this parameter to 0 in releases earlier than Database 4.9.0 is not supported and may trigger immediate evictions.

Renamed in Database 7.0.0 to [`evict-mounts-pct`](https://aerospike.com/docs/database/reference/config#namespace__evict-mounts-pct)

---

#### `mounts-size-limit`

`enterprise` `required` `dynamic`

Context: namespace

Subcontext: index-type flash, sindex-type flash, index-type pmem, sindex-type pmem

Description: Maximum amount of total device space for the mount(s) on this namespace. For example, if there are two mount points of 100GiB each, then `mounts-size-limit` should be set to 200GiB. The minimum size is 4GiB and maximum is to not exceed to the total capacity of all mount point\[s\]. This does not prevent sprigs from being allocated beyond the limit, but rather enforces the eviction of records based on the [`mounts-high-water-pct`](https://aerospike.com/docs/database/reference/config#namespace__mounts-high-water-pct) configuration which is measured against the index usage (based on the number of records rather than the number of sprigs). See [All Flash capacity sizing](https://aerospike.com/docs/database/manage/planning/capacity/#primary-index-on-flash) for further details.

Required to be explicitly set when using [`index-type flash`](https://aerospike.com/docs/database/reference/config#namespace__index-type) or [`index-type pmem`](https://aerospike.com/docs/database/reference/config#namespace__index-type).

Introduced: 4.3.0.2 (flash) 4.5.0.1 (pmem), 6.3.0 (sindex-type pmem)

Removed: 7.0.0

Default Value: \-

Detail:
**Example:** Dynamically change mount size limit:

```plaintext
asinfo -v "set-config:context=namespace;id=bar;mounts-size-limit=5368709180"
```

Changing this parameter dynamically does not require a sub-context to be included. Supported size notation is no suffix for bytes, K for Kibibyte (KiB), M for Mebibyte (MiB), G for Gibibyte (GiB), T for Tebibyte (TiB), P for Pebibyte (PiB).

Renamed in Database 7.0.0 to [`mounts-budget`](https://aerospike.com/docs/database/reference/config#namespace__mounts-budget).

---

#### `mrt-duration`

`enterprise` `dynamic` `cloud`

Context: namespace

Description: The default duration of a transaction, in seconds, if a value isn’t specified by the client. Determines the deadline after which commands are no longer permitted as part of a transaction. Minimum 1, maximum 120, default 10 (in seconds).

Introduced: 8.0.0

Removed: \-

Default Value: 10

---

#### `namespace`

`static` `cloud`

Context: namespace

Description: **Note**: this is `namespace` _in the namespace context_, not `namespace` in the XDR context. [Search for `namespace`](https://aerospike.com/docs/database/reference/config#namespace), and look at the **Context** heading to make sure you are working with the correct parameter.  
  
Defines a namespace. For more information, see [Namespace Configuration](https://aerospike.com/docs/database/manage/namespace).

Introduced: \-

Removed: \-

Default Value: \-

Detail:
**Example:** To define namespace someNameSpaceName:

```asciidoc
...

namespace someNameSpaceName {

  ...

  memory-size 256G

  replication-factor 2

  storage-engine device {

    ...

    ...

  }

}

...
```

There is a limit on the number of namespaces in a cluster. See [Upper Sizing Bounds and Naming Constraints](https://aerospike.com/docs/database/reference/limitations).

---

#### `ns-forward-xdr-writes`

`dynamic`

Context: namespace

Description: In Aerospike 5.0.0, this parameter was replaced by [`forward`](https://aerospike.com/docs/database/reference/config#xdr__forward). This parameter provides fine grained control at namespace level to forward writes that originated from another XDR to the specified destination datacenters (in xdr section). This parameter is effective when the [forward-xdr-writes](https://aerospike.com/docs/database/reference/config#xdr__forward-xdr-writes) in the xdr section is set to false. If the forward-xdr-writes in xdr section is set to true, all the namespaces will be forwarded irrespective of the namespace-level setting (ns-forward-xdr-writes).

Introduced: 3.3.26

Removed: 5.0.0

Default Value: false

Detail:
**Example:** Enable ns-forward-xdr-writes on the namespace:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;ns-forward-xdr-writes=true"
```

To dynamically change you must target ASD’s service port, not XDR.

If setting to ‘true’ be aware of your topology and ensure you aren’t creating a forwarding loop.

---

#### `nsup-hist-period`

`dynamic` `cloud`

Context: namespace

Description: The interval (secs) at which the object size histograms, as well as the time-to-live (ttl) histogram, are updated. Setting `nsup-hist-period` to a value of 0 will disable these histogram updates. See the [`histogram`](https://aerospike.com/docs/database/reference/info#histogram) info command for further details on the object size and ttl histograms.

Introduced: 4.5.1

Removed: \-

Default Value: 3600

Detail:
If `nsup-hist-period` is set to zero dynamically, subsequent info commands to get an object size or ttl histogram will, if any exist, return the last histogram generated.

---

#### `nsup-period`

`dynamic` `cloud`

Context: namespace

Description: The interval at which the main expiration/eviction thread (called _NSUP_, the namespace supervisor) wakes up to process the namespace. The default value of `nsup-period` 0 disables the namespace supervisor for the namespace.  
  
By default, the value is in seconds. You can also set this value in minutes, hours, or days, with notation like `1m` or `1h` or `1d`. For additional discussion, see [Namespace Data Retention Configuration](https://aerospike.com/docs/database/manage/namespace/retention).

Introduced: 4.5.1

Removed: \-

Default Value: 0

Detail:
**Example:** Set `nsup-period` to 600 seconds dynamically for a namespace:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;nsup-period=600"
```

If `nsup-period` is dynamically set to zero while NSUP is working, NSUP will finish its current cycle and then become dormant.

Verify that time is synchronized across nodes in a cluster. For Database 4.5.1 or later, for each namespace where NSUP is enabled (that is, `nsup-period` not zero), writes are suspended if cluster clock skew exceeds 40 seconds. Verify that the Network Time Protocol (NTP) or other time synchronization mechanism is installed, configured, and functioning properly.

Prior to Database 4.9.0, the default was 120.

Starting with Database 4.9.0, _the server will not start_ if `nsup-period` is 0 (the default) but [`default-ttl`](https://aerospike.com/docs/database/reference/config#namespace__default-ttl) is non-zero, unless [`allow-ttl-without-nsup`](https://aerospike.com/docs/database/reference/config#namespace__allow-ttl-without-nsup) is set true.

Starting with Database 6.3.0, if the NSUP cycle takes longer than 2 hours and deletes more than 1% of the namespace, it writes a warning line to the [server log](https://aerospike.com/docs/database/reference/logs#nsup__1326802519).

---

#### `nsup-threads`

`dynamic` `cloud`

Context: namespace

Description: The number of dedicated expiration/eviction threads for NSUP to use when processing the namespace. Must be at least 1, and at most 128.

Introduced: 4.5.1

Removed: \-

Default Value: 1

Detail:
**Example:** Set nsup-threads to 3 dynamically for a namespace:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;nsup-threads=3"
```

If nsup-threads is dynamically changed while nsup is working, nsup will finish its current cycle and then apply the new thread count with the next cycle.

---

#### `num-partitions`

`static`

Context: namespace

Subcontext: si

Description: Configuration to alter the number of secondary index trees that are used for query lookups.

Introduced: \-

Removed: 6.1.0

Default Value: 32

Detail:
Increasing this configuration reduces depth of sindex trees, and may help secondary index lookups perform better. However, increasing these will also result in memory overheads, so it is recommended to monitor the memory utilization and benchmark when tuning this configuration.

---

#### `partition-tree-sprigs`

`static` `cloud`

Context: namespace

Description: Number of tree _sprigs_ per partition to use. Default value is 256. Must be an exact power of 2.

For workloads potentially requiring more (values higher than 32K), Enterprise Edition licensees should contact Aerospike support for guidance. Even if the memory overhead seems acceptable, configuring too many sprigs could adversely affect a cluster, such as longer shutdown.

-   A sub-cluster would have to accommodate for all the sprigs that were in the larger cluster (except if [min-cluster-size](https://aerospike.com/docs/database/reference/config#service__min-cluster-size) has been configured to prevent the formation of such sub-cluster).
    
-   The memory required would also have to be contiguous (fragmented memory may prevent the allocation of memory).
    
-   Having too many sprigs on a node could delay shut down and cause an unnecessary cold restart upon the subsequent restart.
    

**Changing this configuration parameter will force a cold start.** Providing more trees (sprigs) reduces the number of levels and speeds up the search. It also causes the reduce lock blockage to be broken up (the reduce lock is unlocked between each sprig, and a sprig takes much less time to traverse than a single partition tree).

Introduced: 3.1.01.0

Removed: \-

Default Value: 256

Detail:
**Example:** A 4-node cluster, `replication-factor` 2, 2048 `partition-tree-sprigs`. **For Database 4.2.0 and later, the per-node namespace memory overhead for sprigs is:**

```plaintext
Community Edition:  64K + (8M x 2 + 8B x 2048 x 4096 x 2) / 4  = 64K + 4M + 32M = 36.06M

Enterprise Edition: 64K + (8M x 2 + (8B + 5B) x 2048 x 4096 x 2) / 4 = 64K + 4M + 32M + 20M = 56.06M
```

**For releases prior to 4.2, the per-node namespace memory overhead for sprigs is:**

```plaintext
Community Edition:  64K + 2.5M + 128M = 130.56M

Enterprise Edition: 64K + 2.5M + 128M + 40M = 170.56M
```

**Database 4.2.0 and later:**

-   Sprigs have a default and minimum value of 256, as high as 256M.
-   Each sprig is 8 bytes. Additionally, the Enterprise Edition also requires 5 bytes for each sprig.
-   Sprigs and locks are only allocated for partitions that are owned by the node. As a cluster gets bigger, the overhead per node decreases.
-   Users who can afford the extra memory overhead should change this to at least 256 (overhead of 21M). Changing this parameter forces a cold start. To anticipate future growth, may go all the way to the maximum of 4096 (336M overhead). :::

---

#### `post-write-cache`

`dynamic` `cloud`

Context: namespace

Subcontext: storage-engine device

Description: The amount of bytes per-device used to cache the recently written write-blocks of this namespace. Should be a multiple of 8MiB, and has a default value of 256MiB.

The `post-write-cache` benefits XDR, as all writes are quasi-immediately read to be shipped to the destination cluster(s). The [`read-page-cache`](https://aerospike.com/docs/database/reference/config#namespace__read-page-cache) configuration parameter can also help to leverage page cache, and help with latency for read intensive workloads. The namespace cache-hit is reflected in its [`cache_read_pct`](https://aerospike.com/docs/database/reference/metrics#namespace__cache_read_pct) statistic.

Also, wblocks in the `post-write-cache` are not eligible to be defragmented. Therefore the `post-write-cache` should be kept small compared to the overall device size as the size allocated to the `post-write-cache` will not be defragmented.

Replaces [`post-write-queue`](https://aerospike.com/docs/database/reference/config#namespace__post-write-queue) in Database 7.1.0 and later. To convert the configuration of an earlier version, set `post-write-cache` to `post-write-queue` multiplied by the `write-block-size`.

Introduced: 7.1.0

Removed: \-

Default Value: 256M

Detail:
Supported size notation is no suffix for bytes, `K` for KiB, `M` for MiB, `G` for GiB.

Example: Set `post-write-cache` per-device to 512MiB:

Terminal window

```bash
asinfo -v 'set-config:context=namespace;id=ns1;post-write-cache=512M'
```

In `asadm` the equivalent is:

Terminal window

```bash
Admin> enable

Admin+> manage config namespace ns1 param post-write-cache to 512M
```

---

#### `post-write-queue`

`dynamic`

Context: namespace

Subcontext: storage-engine device

Description: Removed in Database 7.1.0. Use [`post-write-cache`](https://aerospike.com/docs/database/reference/config#namespace__post-write-cache).

Number of write-block buffers to keep as cache (per device). Only available for non `data-in-memory` storage configurations. Maximum allowed value for Database 4.7.0 and later is 8192. See the [`cache_read_pct`](https://aerospike.com/docs/database/reference/metrics#namespace__cache_read_pct) value for how much of the read workload is being served by the post-write queue. XDR use cases should leverage the `post-write-queue` as writes would be quasi-immediately read to be shipped to the destination cluster(s). The [`read-page-cache`](https://aerospike.com/docs/database/reference/config#namespace__read-page-cache) configuration parameter can also be considered to leverage page cache and help with latency for read-intensive workloads.

Also, wblocks in the `post-write queue` are not eligible to be defragmented. Therefore the `post-write-queue` should be kept small compared to the overall device size as the size allocated to the `post-write-queue` will not be defragmented.

Introduced: \-

Removed: 7.1.0

Default Value: 256

Detail:
**Example:** Set `post-write-queue` to 512:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;post-write-queue=512"
```

Memory allocation for this depends on the `write-block-size` and number of devices. For example, on a namespace with 2 devices and a 128KiB write block size, the default memory allocated will be 2 x 256 x 128KiB. For example, for 2 devices, setting the value to 2048 will use 2 x 2048 x 128KiB (512MiB). Setting `post-write-queue` to 0 disables it.

---

#### `prefer-uniform-balance`

`enterprise` `unanimous` `dynamic` `cloud`

Context: namespace

Description: If true, this namespace will make an effort to distribute partitions evenly to all nodes. Starting with Database 4.7.0 the default value is true. To achieve uniform-balance, Aerospike must give up some migration performance for this namespace. Time required to complete migrations is only impacted when a node is either permanently added or removed; i.e., the time to complete migrations when a restarted node rejoins the cluster is not impacted.

**Has to be followed by a [`recluster`](https://aerospike.com/docs/database/reference/info#recluster) command to be effective.**

For [`strong-consistency`](https://aerospike.com/docs/database/reference/config#namespace__strong-consistency) enabled namespaces, uniform-balance is computed for all nodes in the roster - if a node is offline, the balance will be less uniform (but likely better than without uniform-balance enabled). If the node is permanently down, or down for an extended duration, the administrator may choose to remove the offline node from the roster and issue a [`recluster`](https://aerospike.com/docs/database/reference/info#recluster) command to readjust the partition distribution back to a uniform-balance.

Introduced: 4.3.0.2

Removed: \-

Default Value: true

Detail:
**Example:** Enable `prefer-uniform-balance` on the namespace:

```asciidoc
Admin+> asinfo -v "set-config:context=namespace;id=namespaceName;prefer-uniform-balance=true"

aero-node1:3000 (10.0.3.41) returned:

ok

aero-node2:3000 (10.0.3.224) returned:

ok

aero-node4:3000 (10.0.3.196) returned:

ok

aero-node3:3000 (10.0.3.149) returned:

ok

Admin+> asinfo -v "recluster:"

aero-node1:3000 (10.0.3.41) returned:

ok

aero-node2:3000 (10.0.3.224) returned:

ignored-by-non-principal

aero-node4:3000 (10.0.3.196) returned:

ignored-by-non-principal

aero-node3:3000 (10.0.3.149) returned:

ignored-by-non-principal
```

If any node in the cluster does not have the `prefer-uniform-balance` set to `true`, the cluster reverts to not using the uniform balance scheme.

For Database 4.3.0.2 to 4.3.0.9, enabling `prefer-uniform-balance` on cluster sizes which are a power of 2 (2, 4, 8, 16, etc) would cause migrations to be stuck.

Prior to Database 4.7.0, enabling `prefer-uniform-balance` in AP namespaces and not waiting for delta migrations to complete between node restarts in a rolling restart could cause non-optimal masters may be selected (which could lead to extra duplicate resolution on writes, and extra stale reads if read duplication resolution is not enabled).

---

#### `rack-id`

`enterprise` `dynamic`

Context: namespace

Description: Designates which rack this node should be a part of. `rack-id` must be an integer between 0 and 1000000. For [`strong-consistency`](https://aerospike.com/docs/database/reference/config#namespace__strong-consistency) namespaces, the `rack-id` configuration is set through the roster itself. See [Configure rack awareness in strong consistency mode](https://aerospike.com/docs/database/manage/namespace/consistency/#rack-awareness) for more information.

Introduced: 3.13.0.1 (post cluster protocol change)

Removed: \-

Default Value: 0

Detail:
**Example:**

```asciidoc
rack-id 1
```

Set `rack-id` to 2 dynamically:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;rack-id=2"
```

Set `rack-id` for multiple nodes at once:

```plaintext
Admin+> asinfo -v "set-config:context=namespace;id=test;rack-id=101" with 192.168.10.2 192.168.10.4 192.168.10.5

node2.aerospike.com:3000 (192.168.10.2) returned:

ok

node4.aerospike.com:3000 (192.168.10.4) returned:

ok

node5.aerospike.com:3000 (192.168.10.5) returned:

ok
```

Set `rack-id` for strong consistency:

```plaintext
Admin+> asinfo -v "roster-set:namespace=test;nodes=BB9070016AE4202@102,BB9060016AE4202@101,BB9050016AE4202@101,BB9040016AE4202@101,BB9020016AE4202@102

node2.aerospike.com:3000 (192.168.10.2) returned:

ok

...

Admin+> asinfo -v "recluster:"

...
```

---

#### `read-consistency-level-override`

`dynamic` `cloud`

Context: namespace

Description: When set to a non-default value, overrides the client-specified per-transaction read consistency level for this namespace. This configuration specifies whether the server is to consult internally the different versions of a record to determine the most-recent record value when duplicate resolving in an ongoing migration.  
Values: `off`, `one`, `all`.  
See the discussion of SC guarantee in [Strong Consistency Mode](https://aerospike.com/docs/database/learn/architecture/clustering/consistency-modes#sc-mode).

Introduced: 3.3.26

Removed: \-

Default Value: off

Detail:
**Example:** Set read consistency level override to one in the configuration file (skip duplicate resolution):

```asciidoc
read-consistency-level-override one
```

Dynamically override clients and set read consistency to one:

```asciidoc
asinfo -v "set-config:context=namespace;id=namespaceName;read-consistency-level-override=one"
```

[`strong-consistency`](https://aerospike.com/docs/database/reference/config#namespace__strong-consistency) enabled namespaces always duplicate resolve when migrations are ongoing and consult the different potential versions of a record before returning to the client. This configuration is therefore not available for [`strong-consistency`](https://aerospike.com/docs/database/reference/config#namespace__strong-consistency) enabled namespaces.

---

#### `read-page-cache`

`dynamic` `cloud`

Context: namespace

Subcontext: storage-engine device

Description: If `true`, disables the odirect and odsync flags during read transactions. This allows the OS to leverage page cache and can help with latencies for some workload types. Should be tested or deployed on a single node prior to full production roll out. This configuration should not be set `true` for namespaces with [`data-in-memory`](https://aerospike.com/docs/database/reference/config#namespace__data-in-memory) set `true`. It may be useful to set `read-page-cache` to `true` if using raw devices, or if using file storage with `data-in-memory` set `false` and [`direct-files`](https://aerospike.com/docs/database/reference/config#namespace__direct-files) or [`commit-to-device`](https://aerospike.com/docs/database/reference/config#namespace__commit-to-device) set `true`. See the [Buffering and Caching in Aerospike](https://support.aerospike.com/s/article/Buffering-and-Caching-in-Aerospike) article for further details.

Introduced: 4.3.1

Removed: \-

Default Value: false

Detail:
**Example:** Set read-page-cache to true dynamically:

```asciidoc
asinfo -v "set-config:context=namespace;id=namespaceName;read-page-cache=true"
```

Performant storage sub-systems running on older kernels may be adversely impacted by this setting as checking the page cache prior to accessing the storage sub-system may be penalizing.  
Workload with higher [`cache_read_pct`](https://aerospike.com/docs/database/reference/metrics#namespace__cache_read_pct) may be considered, but should also check the impact of increasing the [`post-write-cache`](https://aerospike.com/docs/database/reference/config#namespace__post-write-cache) configuration parameter. Less performant storage sub-systems (network attached for example) may greatly benefit from disabling the odirect and odsync flags.

Using `read-page-cache` when the read workload is very uniform (no hotkey type patterns) may not be beneficial and could lead into spending unnecessary CPU cycles, which should usually be negligible.

---

#### `reject-non-xdr-writes`

`enterprise` `dynamic` `cloud`

Context: namespace

Description: Parameter to control the writes done by a non-XDR client. Setting it to true disallows writes from a non-XDR client (any regular client library).  
  
This parameter is on the destination or target node in the `namespace` stanza, not the `xdr` stanza’s `dc`’s `namespace` sub-stanza.  
  
This parameter is useful to control accidental writes by a non-XDR client to a namespace when it is not expected, and can be used for namespaces taking writes exclusively from XDR clients. When set to true, error code 10 will be returned and will tick the [`fail_xdr_forbidden`](https://aerospike.com/docs/database/reference/metrics#namespace__fail_xdr_forbidden) statistic.

Introduced: 5.0.0

Removed: \-

Default Value: false

Detail:
**Example:** Namespace stanza on XDR destination:

```plaintext
namespace someNameSpaceName {

  reject-non-xdr-writes true

  ...

}
```

Set `reject-non-xdr-writes` to true:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;reject-non-xdr-writes=true"
```

---

#### `reject-xdr-writes`

`enterprise` `dynamic` `cloud`

Context: namespace

Description: Parameter to control whether to accept write transactions originating from an XDR client. Setting it to true disallows all the writes from an XDR client (at a destination cluster) and allow only non-XDR clients to write transactions.  
  
This parameter is on the destination or target node in the `namespace` stanza, not the `xdr` stanza’s `dc`’s `namespace` sub-stanza.  
  
This parameter is useful to control accidental writes by an XDR client. When set to true, error code 10 will be returned, disallowed writes will not be relogged by XDR and will tick the [`fail_xdr_forbidden`](https://aerospike.com/docs/database/reference/metrics#namespace__fail_xdr_forbidden) statistic on the remote (destination) cluster.

Introduced: 5.0.0

Removed: \-

Default Value: false

Detail:
**Example:** Namespace stanza on XDR destination:

```asciidoc
namespace someNameSpaceName {

  reject-xdr-writes true

  ...

}
```

Set `reject-xdr-writes` to true:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;reject-xdr-writes=true"
```

---

#### `replication-factor`

`unanimous` `dynamic` `cloud`

Context: namespace

Description: Unanimous configuration, specifies the number of copies of a record (including the master copy) maintained in the entire cluster. AP namespaces can be dynamically modified, followed by a [`recluster`](https://aerospike.com/docs/database/reference/info?ver=7&q=recluster#recluster) info command to make the changes take effect. The [`effective_replication_factor`](https://aerospike.com/docs/database/reference/metrics#namespace__effective_replication_factor) drops automatically if the number of nodes in the cluster is less than the RF. Prior to Database 7.2.0, the RF factor drops when a node shuts down or crashes, and the remaining nodes are fewer than the RF. In Database 7.2.0 this will happen as soon as a node is quiesced and there are fewer nodes in the cluster than the RF.

The effective replication factor is 0 for an orphaned node. For example, if a node tries to join a cluster but that node is unable to communicate with every other node in the cluster, the principal node rejects the request and the node marks itself as an [orphan](https://aerospike.com/docs/database/reference/logs#exchange__1120692644).

For SC namespaces, which are configured with [`strong-consistency`](https://aerospike.com/docs/database/reference/config#namespace__strong-consistency) set to `true`, the RF can only be modified statically and unanimously, essentially through a cluster wide shutdown and restart. If the cluster has fewer nodes than the RF, the effective replication factor drops to 0, and the namespace partitions become unavailable.

Introduced: \-

Removed: \-

Default Value: 2

Detail:
**Example:** In Database 6.0.0 and later, you can set the replication factor dynamically in AP namespaces:

```plaintext
Admin+> manage config namespace test param replication-factor to 3

Admin+> manage recluster
```

This example uses `asadm` to change the entire cluster’s replication factor. The `asinfo` CLI tool only sends commands to one node at a time.

In Database 6.0.0 and later, `replication-factor` is dynamic for AP namespaces (non [`strong-consistency`](https://aerospike.com/docs/database/reference/config#namespace__strong-consistency)).

For AP namespaces in Database 6.0.0 and later, `replication-factor` can be changed dynamically. A `recluster` command is required for the change to take effect. Prior to Database 6.0.0, changes to `replication-factor` require a full cluster restart.

---

#### `scheduler-mode`

`static`

Context: namespace

Subcontext: storage-engine device

Description: Optional I/O scheduler for non-NVMe drives (SSD or HDD).

Introduced: \-

Removed: 6.4.0

Default Value: (set by system)

Detail:
See [FAQ - What is the purpose of setting the disk scheduler?](https://discuss.aerospike.com/t/faq-what-is-the-purpose-of-setting-the-disk-scheduler/3680).

---

#### `serialize-tomb-raider`

`enterprise` `static` `cloud`

Context: namespace

Subcontext: storage-engine device

Description: Prevent tomb raids in different namespaces from running concurrently.

Introduced: 4.3.0 (device)

Removed: \-

Default Value: false

Detail:
This configuration is not available in `storage-engine memory` or `storage-engine pmem`.

---

#### `set-delete`

`unanimous` `dynamic`

Context: namespace

Description: Replaced by info command `truncate` starting with Database 3.12.0. See the [truncate info command](https://aerospike.com/docs/database/reference/info#truncate) for details. Setting it to true will delete the specified set in the namespace. Resets to false after deletion occurs.  
For more information on deleting sets, see [Managing Sets](https://aerospike.com/docs/database/manage/namespace/sets)

Introduced: 3.6.1

Removed: 3.1.02.0

Default Value: false

Detail:
**Example:** Enable set-delete on the set:

```asciidoc
asinfo -v "set-config:context=namespace;id=namespaceName;set=setname;set-delete=true"
```

---

#### `set-disable-eviction`

`unanimous` `dynamic`

Context: namespace

Subcontext: set

Description: Setting it to true will protect the set from evictions. Setting this parameter does not affect the TTL of records within the set. Records can have a TTL and will expire as normal.

Introduced: 3.6.1

Removed: 5.6.0

Default Value: false

Detail:
**Example:** Enable set-disable-eviction on the set:

```asciidoc
asinfo -v "set-config:context=namespace;id=namespaceName;set=setname;set-disable-eviction=true"

/* Setting parameter under namespace definition in a static manner.

  set set1 {

           set-disable-eviction true

  }

  set set2 {

           set-disable-eviction true

  }

  set test {

           set-disable-eviction true

  }
```

Eviction may well happen at startup and, as such, it is good practice to enter protected sets into aerospike.conf as shown above to prevent a protected set being evicted during cold start. This parameter was renamed to [`disable-eviction`](https://aerospike.com/docs/database/reference/config#namespace__disable-eviction)in Database 5.6.0.

---

#### `set-enable-xdr`

`dynamic`

Context: namespace

Subcontext: set

Description: Replaced in Aerospike 5.0.0 by [`ship-only-specified-sets`](https://aerospike.com/docs/database/reference/config#xdr__ship-only-specified-sets) and [`ignore-set`](https://aerospike.com/docs/database/reference/config#xdr__ignore-set).  
  
Set-specific parameter to enable/disable shipping through XDR.

Introduced: \-

Removed: 5.0.0

Default Value: use-default

Detail:
If set to ‘use-default’, it inherits the behavior from sets-enable-xdr. If set to ‘true’, XDR will ship this set (overriding sets-enable-xdr). If set to ‘false’, XDR will not ship this set (overriding sets-enable-xdr).

**Example:** Changing set-enable-xdr dynamically:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;set=setname;set-enable-xdr=true"

asinfo -v "set-config:context=namespace;id=namespaceName;set=setname;set-enable-xdr=false"
```

---

#### `set-stop-writes-count`

`dynamic`

Context: namespace

Subcontext: set

Description: How many records may be in this set before the server begins rejecting writes to this set.

This parameter was renamed to [`stop-writes-count`](https://aerospike.com/docs/database/reference/config#namespace__stop-writes-count) in Database 5.6.0.

Introduced: 3.7.0.1

Removed: 5.6.0

Default Value: 0 (Disabled)

Detail:
The `set-stop-writes-count` parameter will only take effect when the number of records reaches the threshold configured. Once the threshold is reached, clients will get Error Code 22 (AEROSPIKE\_ERR\_FAIL\_FORBIDDEN) back.

**Example:** Dynamically set the count to two thousands:

```asciidoc
asinfo -v "set-config:context=namespace;id=namespaceName;set=setname;set-stop-writes-count=2000"
```

---

#### `set`

`static` `cloud`

Context: namespace

Description: Begins a set context, set must be followed by the set name.

Introduced: \-

Removed: \-

Default Value: \-

---

#### `sets-enable-xdr`

`dynamic`

Context: namespace

Description: Replaced in Aerospike 5.0.0 by [`ship-only-specified-sets`](https://aerospike.com/docs/database/reference/config#xdr__ship-only-specified-sets).  
  
Specifies whether XDR should ship all sets in a namespace or not.

Introduced: \-

Removed: 5.0.0

Default Value: true

Detail:
This setting can be overridden at set level by the set-enable-xdr parameter.

**Example:** Set sets-enable-xdr dynamically to false:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;sets-enable-xdr=true"
```

---

#### `sindex-stage-size`

`static` `cloud`

Context: namespace

Description: Configuration used to size the secondary index arena(s).

Introduced: 6.1.0

Removed: \-

Default Value: 1G

Detail:
Configuration must be a power of 2. Lower limit is 128M and maximum value is 4G. Memory limit is max of 8TiB. This setting changes the size of each of the 2048 possible arena stages, for all editions (CE/EE/SE).

Supported size notation is no-suffix for bytes, K for Kibibyte (KiB), M for Mebibyte (MiB), G for Gibibyte (GiB), T for Tebibyte (TiB), P for Pebibyte (PiB).

---

#### `sindex-startup-device-scan`

`static` `cloud`

Context: namespace

Subcontext: storage-engine device

Description: At startup, build secondary indexes by scanning devices.  
  
If most records in the namespace are in sets with secondary indexes, setting this configuration `true` will very likely speed up the secondary index rebuild. Whether this will be faster also depends on other factors, such as average record size, and number of configured devices. Ultimately, experimentation is the best way to determine whether to set this configuration or not.

Introduced: 5.3.0

Removed: \-

Default Value: false

Detail:
`sindex-startup-device-scan` and [`data-in-memory`](https://aerospike.com/docs/database/reference/config#namespace__data-in-memory) cannot both be configured `true`.

---

#### `sindex-type`

`enterprise` `static`

Context: namespace

Description: Options: shmem, pmem, flash

If `shmem`, secondary indexes are stored in Linux shared memory.

If `pmem`, the secondary indexes are stored in persistent memory (e.g., Intel Optane DC Persistent Memory).

If `flash`, the secondary indexes are stored in a block storage device (typically NVMe SSD).

In all options, the node is able to [fast-restart](https://aerospike.com/docs/database/manage/database/fast-start). If `pmem` or `flash`, the secondary indexes are also preserved across reboots of the node’s OS, allowing for fast-restart after the host machine reboots.

Setting to `pmem` needs the `asdb-pmem` feature-key, setting to `flash` requires the `asdb-flash-index` feature-key to be enabled in the [`feature-key-file`](https://aerospike.com/docs/database/manage/planning/feature-key).  
For information about `shmem`, `pmem`, and `flash`, see [Configuring the secondary index](https://aerospike.com/docs/database/manage/namespace/secondary-index).

Introduced: 6.3.0 (pmem), 6.4.0 (flash)

Removed: \-

Default Value: shmem

Detail:
On Community Edition, this will appear as ‘undefined’ and is not configurable.

---

#### `single-bin`

`unanimous` `static`

Context: namespace

Description: Setting it true will disallow multiple bin (columns) for a record.

Introduced: \-

Removed: 6.4.0

Default Value: false

Detail:
Used to save storage space and provide enhanced performance on update transactions where prior read is not required. Transactions such as List append, Map key-value update or increment operation still require a read. Requires storage reinitialization. Single-bin with data-in-memory does not allow storing user key (sendKey true). To store user-key with single-bin, storage must not configure data-in-memory true. For UDF transactions against single-bin namespaces, the bin name is required to be an empty string for reading or writing the bin. For further recommendation for this parameter, contact Aerospike.

---

#### `single-query-threads`

`dynamic` `cloud`

Context: namespace

Description: Maximum number of threads allowed for a single query. Value range: 1-128.

Introduced: 6.0.0

Removed: \-

Default Value: 4

Detail:
**Example:** Set single-query-threads to 12:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;single-query-threads=12"
```

---

#### `single-scan-threads`

`dynamic`

Context: namespace

Description: Maximum number of threads allowed for a single query. Value range: 1-128.

Introduced: 4.7.0

Removed: 6.0.0

Default Value: 4

Detail:
**Example:** Set single-scan-threads to 12:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;single-scan-threads=12"
```

This parameter was renamed to [`single-query-threads`](https://aerospike.com/docs/database/reference/config#namespace__single-query-threads)in Database 6.0.0

---

#### `stop-writes-avail-pct`

`dynamic` `cloud`

Context: namespace

Subcontext: storage-engine

Description: Disallow writes except deletes, replica writes and migration writes when [`data_avail_pct`](https://aerospike.com/docs/database/reference/metrics#namespace__data_avail_pct) on one of the devices or pmem files or memory storage configured for the namespace is below this specified percentage.

Introduced: 7.0.0

Removed: \-

Default Value: 5

Detail:
Writes are disallowed when memory utilization for the namespace reaches the configured:

-   [`stop-writes-used-pct`](https://aerospike.com/docs/database/reference/config#namespace__stop-writes-used-pct), or
-   [`stop-writes-sys-memory-pct`](https://aerospike.com/docs/database/reference/config#namespace__stop-writes-sys-memory-pct).

We do not recommend setting this value below 5%. Doing so may not allow enough buffer room for replica writes and migrations writes. This may lead to not having enough free blocks for defrag to recover the system, in which case the node would need to cold start to recover.

---

#### `stop-writes-count`

`dynamic` `cloud`

Context: namespace

Subcontext: set

Description: How many records may be in this set before the server begins rejecting writes to this set.

Introduced: 5.6.0

Removed: \-

Default Value: 0 (Disabled)

Detail:
The `stop-writes-count` parameter will only take effect when the number of records reaches the threshold configured. Once the threshold is reached, clients will get Error Code 22 (AEROSPIKE\_ERR\_FAIL\_FORBIDDEN) back.

**Example:** Configure a set-specific `stop-writes-count` value within the namespace configuration context:

```asciidoc
set setname {

           stop-writes-count 1000

  }
```

Dynamically set the count to two thousand:

```asciidoc
asinfo -v "set-config:context=namespace;id=namespaceName;set=setName;stop-writes-count=2000"
```

This parameter was renamed from [`set-stop-writes-count`](https://aerospike.com/docs/database/reference/config#namespace__set-stop-writes-count) in Database 5.6.0.

---

#### `stop-writes-pct`

`dynamic`

Context: namespace

Description: Disallow writes when memory utilization (tracked under [`memory_used_bytes`](https://aerospike.com/docs/database/reference/metrics#namespace__memory_used_bytes)) is greater than this specified percentage:

-   This threshold is checked every 10 seconds.
-   Deletes, replica writes, and migration writes are still allowed.

Introduced: \-

Removed: 7.0.0

Default Value: 90

Detail:
**Example:** Set stop-writes-pct to 95:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;stop-writes-pct=95"
```

Writes are also disallowed when one of the namespace’s device available percent on disk gets down to [`min-avail-pct`](https://aerospike.com/docs/database/reference/config#namespace__min-avail-pct). See the [`stop_writes`](https://aerospike.com/docs/database/reference/metrics#namespace__stop_writes) and [`clock_skew_stop_writes`](https://aerospike.com/docs/database/reference/metrics#namespace__clock_skew_stop_writes) metrics for more details on the situations leading to putting a node in read only mode.

---

#### `stop-writes-size`

`dynamic` `cloud`

Context: namespace

Subcontext: set

Description: Specifies a maximum limit in bytes for the size of a set. For [data-in-memory namespaces](https://aerospike.com/docs/database/manage/namespace/storage/config), this limit is for [`memory_data_bytes`](https://aerospike.com/docs/database/reference/metrics#sets__memory_data_bytes). For other types of storage, the limit is for [`device_data_bytes`](https://aerospike.com/docs/database/reference/metrics#sets__device_data_bytes). After the limit is reached, the server does not allow any additional writes, even those that would decrease the size of a record. There are two ways to get under the `stop-writes-size` limit: increase or remove the limit, or delete records.

When the `stop-writes-size` limit is breached, the server rejects record deletions via UDF, delete-all-bins operations, and background operations. The server allows only regular delete operations and namespace supervisor (NSUP) delete operations in this situation. The server writes warnings to the log for rejected transactions. When the set size falls back below the `stop-writes-size` limit, normal delete behavior is resumed.

The [sets](https://aerospike.com/docs/database/reference/info#sets) info command outputs the `stop-writes-size` configuration in bytes, as well as the [`device_data_bytes`](https://aerospike.com/docs/database/reference/metrics#sets__device_data_bytes) or [`memory_data_bytes`](https://aerospike.com/docs/database/reference/metrics#sets__memory_data_bytes) set metrics. By comparing those values, a monitoring/management tool can determine if the set is currently unable to accept writes due to a quota violation.

Introduced: 6.3.0

Removed: \-

Default Value: 0 (no limit)

Detail:
Supported size notation is no suffix for bytes, K for Kibibyte (KiB), M for Mebibyte (MiB), G for Gibibyte (GiB), T for Tebibyte (TiB), P for Pebibyte (PiB).

**Example:** Configure a set-specific `stop-writes-size` value within the namespace configuration context:

```asciidoc
set setname {

           stop-writes-size 500M

  }
```

Dynamically enable a set-specific `stop-writes-size` value:

```asciidoc
asinfo -v "set-config:context=namespace;id=namespaceName;set=setName;stop-writes-size=550M"
```

In Database 7.0.0, [`device_data_bytes`](https://aerospike.com/docs/database/reference/metrics#sets__device_data_bytes) and [`memory_data_bytes`](https://aerospike.com/docs/database/reference/metrics#sets__memory_data_bytes) were replaced by [`data_used_bytes`](https://aerospike.com/docs/database/reference/metrics#namespace__data_used_bytes).

---

#### `stop-writes-sys-memory-pct`

`enterprise` `dynamic` `cloud`

Context: namespace

Description: Aerospike monitors the total amount of system memory in use, including non-Aerospike memory usage. If the amount of system memory in use out of the total system memory becomes greater than the specified percentage, new writes are disallowed.

Introduced: 6.3.0

Removed: \-

Default Value: 90

Detail:
Use extreme caution when changing this setting. It exists to protect the system from OOM kills. Increasing this setting past the default value may change it from being a stable but read-only system to an unstable or unavailable system. ::: **Example:** Designate a `stop-writes-sys-memory-pct` value within a namespace definition in the configuration file:

```asciidoc
stop-writes-sys-memory-pct 75
```

Dynamically enable a `stop-writes-sys-memory-pct` value:

```asciidoc
asinfo -v "set-config:context=namespace;id=namespaceName;stop-writes-sys-memory-pct=75"
```

---

#### `stop-writes-used-pct`

`dynamic` `cloud`

Context: namespace

Subcontext: storage-engine

Description: Disallow writes except deletes, durable deletes, replica writes, and migration writes when the ratio of [`data_used_bytes`](https://aerospike.com/docs/database/reference/metrics#namespace__data_used_bytes) to [`data_total_bytes`](https://aerospike.com/docs/database/reference/metrics#namespace__data_total_bytes) for the namespace is greater than this specified percentage.

Introduced: 7.0.0

Removed: \-

Default Value: 70

Detail:
**Example:** Designate a `stop-writes-used-pct` value within a namespace storage-engine definition in the configuration file:

```asciidoc
stop-writes-used-pct 90
```

Dynamically enable a `stop-writes-used-pct` value:

```asciidoc
asinfo -v "set-config:context=namespace;id=namespaceName;stop-writes-used-pct=90"
```

---

#### `storage-engine`

`static`

Context: namespace

Description: Determines whether or not writes are persisted. Required in Database 7.0.0 and later. Accepted values are:

-   `device` - Data written to this node is persisted to either a raw device or a file.
-   `memory` - Data written to this node is written to DRAM. You can also specify one or more `file` or `device` parameters to store a copy of the data. `memory` was the default value for this parameter prior to Database 7.0.0.
-   `pmem` - Data written to this node is written to persistent memory. This requires an EE license and the `asdb-pmem` feature-key to be enabled in the [`feature-key-file`](https://aerospike.com/docs/database/reference/config#service__feature-key-file).

In Database 7.0.0, `index-type flash` does not work with `storage-engine pmem` or `storage-engine memory`.

Introduced: \-

Removed: \-

Default Value: undefined

Detail:
For more information about defining an in-memory only namespace, see [Configure Namespace Storage](https://aerospike.com/docs/database/manage/namespace/storage/config).

---

#### `strict`

`static` `cloud`

Context: namespace

Subcontext: geo2dsphere-within

Description: Additional sanity check from Aerospike to validate whether the points returned by S2 falls under the user’s query region. When set to false, Aerospike does not do this additional check and send the results as it is.

Introduced: 3.7.0.1

Removed: \-

Default Value: true

---

#### `strong-consistency-allow-expunge`

`enterprise` `dynamic` `cloud`

Context: namespace

Description: When set to `true`, allows non-durable deletes to be used with [`strong-consistency`](https://aerospike.com/docs/database/reference/config#namespace__strong-consistency). Expunges are not ‘consistent’.

Introduced: 4.0.0

Removed: \-

Default Value: false

Detail:
**Example:**

```plaintext
Admin+> asinfo -v "set-config:context=namespace;id=bar;strong-consistency-allow-expunge=true"

172.17.0.10:3000 (172.17.0.10) returned:

ok

0e0d1a1651ae:3000 (172.17.0.9) returned:

ok
```

---

#### `strong-consistency`

`enterprise` `static` `cloud`

Context: namespace

Description: Set the namespace to [Strong Consistency](https://aerospike.com/docs/database/manage/namespace/consistency) mode to favor consistency over availability. Allows linearized reads to be enabled. See the [Configuring strong consistency](https://aerospike.com/docs/database/manage/namespace/consistency) and [Consistency Management](https://aerospike.com/docs/database/manage/cluster/consistency) pages for further details.  
Requires the `asdb-strong-consistency` feature-key to be enabled in the [`feature-key-file`](https://aerospike.com/docs/database/reference/config#service__feature-key-file).

Introduced: 4.0.0

Removed: \-

Default Value: false

Detail:
Changing an [Available mode](https://aerospike.com/docs/database/learn/architecture/clustering/consistency-modes#ap-mode) (AP) namespace into a Strong Consistency mode (SC) namespace by simply turning the feature on in the configuration is not supported. In order to create a strongly consistent namespace, the storage needs to be emptied. Migrating into an SC namespace can be done by performing a backup on an AP namespace and restoring into an SC namespace.

---

#### `tomb-raider-eligible-age`

`enterprise` `dynamic` `cloud`

Context: namespace

Description: Number of seconds to retain a tombstone, even though it’s discovered to be safe to remove. This is to protect a cluster from older records to be re-introduced after a node that was out of the cluster for some time joins the cluster back. If a node was out of a cluster for longer than the `tomb-raider-eligible-age`, it should have all of its data removed before being brought back in the cluster. Default is 1 day.

Introduced: 3.10.0

Removed: \-

Default Value: 86400

Detail:
**Example:** Set tomb-raider-eligible-age to 43200 (1/2 day):

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;tomb-raider-eligible-age=43200"
```

---

#### `tomb-raider-period`

`enterprise` `dynamic` `cloud`

Context: namespace

Description: Minimum amount of time, in seconds, between tomb-raider runs. Default is 1 day.

Starting with Database 4.3.0, setting tomb-raider-period to a value of 0 will deactivate tomb raider.

Introduced: 3.10.0

Removed: \-

Default Value: 86400

Detail:
**Example:** Set tomb-raider-period to 43200 (1/2 day):

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;tomb-raider-period=43200"
```

If `tomb-raider-period` is set to zero dynamically while a tomb raid is in progress, the tomb raid will complete and then the tomb raider will become dormant.

---

#### `tomb-raider-sleep`

`enterprise` `dynamic` `cloud`

Context: namespace

Subcontext: storage-engine device or storage-engine pmem or storage-engine memory

Description: Number of microseconds to sleep in between large block reads on disk or pmem storage files. Default is 1 ms (1000µs), max 4,294,967,296 µs.

Introduced: 3.10.0 (device) 4.8.0 (pmem) 7.0.0 (storage-engine memory)

Removed: \-

Default Value: 1000

Detail:
**Example:** Set tomb-raider-sleep to 2000:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;tomb-raider-sleep=2000"
```

---

#### `transaction-pending-limit`

`dynamic` `cloud`

Context: namespace

Description: Maximum pending transactions that can be queued up to work on the same key. A value of 0 removes the limit (unlimited), and a value of 1 will allow a maximum of 1 transaction to be queued up in the rw-hash behind a transaction that is already in progress.

Excessive transactions may result in a `KEY_BUSY` error (14). See “key-busy” in the [Server Log Reference](https://aerospike.com/docs/database/reference/logs#info__994802748).

This parameter context was moved from service to namespace in Database 4.3.1.3.

Introduced: 4.3.1.3

Removed: \-

Default Value: 20

Detail:
**Example:** Set transaction-pending-limit to 3 dynamically:

```asciidoc
asinfo -v "set-config:context=namespace;id=namespaceName;transaction-pending-limit=3"
```

Prior to Database 4.3.1.3, run this instead:

```asciidoc
asinfo -v "set-config:context=service;transaction-pending-limit=3"
```

Increase this limit if the application works on a small set of keys more frequently. If this value is exceeded the overflow transactions will fail and the client will receive an error code 14 Key Busy (tracked on the server side under the [`fail_key_busy`](https://aerospike.com/docs/database/reference/metrics#namespace__fail_key_busy) statistic).

---

#### `truncate-threads`

`dynamic` `cloud`

Context: namespace

Description: The number of dedicated threads each truncate job will create in the namespace. Minimum is 1, maximum is 128. If a truncated set has a set index, this will be used and should speed up the job significantly. However, if the set contains any tombstones at the beginning of the job, the set index cannot be used because set indexes do not include tombstones.

Introduced: 4.6.0

Removed: \-

Default Value: 4

Detail:
**Example:** Set `truncate-threads` dynamically to 6 for a namespace:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;truncate-threads=6"
```

If `truncate-threads` is changed dynamically, any currently active truncation is not affected, and will be effective beginning with the next truncation round. If truncating many sets at the same time, consider tuning this down.  
  
Statistics per job are available in a log line written at the completion of a truncation.  
  

-   Example for set truncation: {ns-name|set-name} done truncate to 12345678 deleted 3456  
      
    
-   Example for namespace truncation: {ns-name} done truncate to 12345678 deleted 3456

---

#### `write-block-size`

`static`

Context: namespace

Subcontext: storage-engine device

Description: Removed as a configuration parameter in Database 7.1.0, as the write-blocks for all `storage-engine` types are hardcoded to 8MiB. Use [`max-record-size`](https://aerospike.com/docs/database/reference/config#namespace__max-record-size), [`flush-size`](https://aerospike.com/docs/database/reference/config#namespace__flush-size), and [`post-write-cache`](https://aerospike.com/docs/database/reference/config#namespace__post-write-cache) to limit the max record size to a value up to 8MiB. In database 7.0.0, `storage-engine` memory has write-block size hard-coded to 8MiB.

Size in bytes of each I/O block that is written to the disk. Effectively sets the maximum object size, which can also be controlled by `max-record-size`. Acceptable values are 128K, 256K, 512K, 1M. Starting with Database 4.2.0, 2M, 4M or 8M. Large `write-block-size` may adversely impact performance. See [“How do I change the write-block-size configuration?”](https://support.aerospike.com/s/article/How-do-I-change-the-write-block-size-configuration) for more information.

Introduced: \-

Removed: 7.1.0

Default Value: 1M

Detail:
Supported size notation is no suffix for bytes, K for Kibibyte (KiB), M for Mebibyte (MiB). This configuration is not available in `storage-engine pmem` with write-block size hard-coded to 8MiB.

---

#### `write-commit-level-override`

`dynamic` `cloud`

Context: namespace

Description: When set to `all` or `master` (AKA _“fire and forget”_), overrides the client-specified [commit-level policy](https://aerospike.com/docs/database/learn/policies/#write-commit-level) for write transactions to this namespace.  
Values: `off`, `all`, `master`.  

Only applies to high availability (AP) namespaces. Not available for [`strong-consistency`](https://aerospike.com/docs/database/reference/config#namespace__strong-consistency) enabled (CP) namespaces because they write (or attempt to write) to all replicas prior to returning to the client.

Introduced: 3.3.26

Removed: \-

Default Value: off

Detail:
**Example:** Set write commit level override to master in the configuration file (return upon master side completion without waiting for replica side):

```asciidoc
write-commit-level-override master
```

Dynamically override clients and set commit level to master for every write transaction in this namespace:

```asciidoc
asinfo -v "set-config:context=namespace;id=namespaceName;write-commit-level-override=master"
```

Starting with Database 5.7.0, this policy has a circuit breaker. When configured to `master` it automatically converts to `all` if the fabric layer cannot keep up with the replication. This change pushes back on the client and protects the service. When configured to `master`, transactions do not wait for the replica write acknowledgement. This avoids potential latency increases when receiving multiple transactions for the same key that would otherwise be queued up on the read/write hash [`rw_in_progress`](https://aerospike.com/docs/database/reference/metrics#node_stats__rw_in_progress).  
  
When configured to `all`, in case of failure to replicate properly, a timeout is returned to the client, but the transaction is not rolled back on the master side. The replica side may or may not have the update based on exactly where the transaction broke between master and replica. This failure could be where the node that owns the master copy is unable to reach a replica, or gets a response even when unable to reach a replica. See [`transaction-max-ms`](https://aerospike.com/docs/database/reference/config#service__transaction-max-ms) for details on this mechanism.

---

#### `xdr-bin-tombstone-ttl`

`enterprise` `dynamic` `cloud`

Context: namespace

Description: If [`bin-policy`](https://aerospike.com/docs/database/manage/xdr/bin-policy) is set to ship changed bins (policies other than the default `all`), bin deletions will create bin tombstones. This parameter specifies the time-to-live (in seconds) for those bin tombstones. 0 means never expire. Bin tombstones whose TTL expired will be removed only on a subsequent write operation on the record. The default value in Database 5.2.x used to be 0 and it changed to 86400 (1 day) as of 5.3.

Introduced: 5.2.0

Removed: \-

Default Value: 86400

Detail:
**Example:** Set xdr-bin-tombstone-ttl to 600 seconds:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;xdr-bin-tombstone-ttl=600"
```

---

#### `xdr-remote-datacenter`

`dynamic`

Context: namespace

Description: As of Aerospike 5.0.0, replaced by the [`dc`](https://aerospike.com/docs/database/reference/config#xdr__dc) parameter.  
  
Name of the datacenter to forward this namespace to.

Introduced: \-

Removed: 5.0.0

Default Value: \-

Detail:
The `xdr-remote-datacenter` parameter should be defined for each remote datacenter XDR is to ship to. This can be set dynamically starting with Database 3.8.1.

The Datacenter names are defined in the XDR stanza.

**Example:** Dynamically associating and disassociating a namespace to a remote datacenter:

```asciidoc
asinfo -v "set-config:context=namespace;id=namespaceName;xdr-remote-datacenter=DC1;action=add"

asinfo -v "set-config:context=namespace;id=namespaceName;xdr-remote-datacenter=DC1;action=remove"
```

It is not safe to dynamically remove a remote datacenter prior to Database 5.x. Contact Aerospike support more information if a datacenter must be dynamically removed in older versions.

---

#### `xdr-tomb-raider-period`

`enterprise` `dynamic` `cloud`

Context: namespace

Description: Minimum amount of time, in seconds, between xdr-tomb-raider runs. Default is 120 seconds. This only applies to [`xdr_tombstones`](https://aerospike.com/docs/database/reference/metrics#namespace__xdr_tombstones) and not regular tombstones from durable deletes. Setting xdr-tomb-raider-period to a value of 0 will deactivate the xdr-tomb-raider.

Introduced: 5.0.0

Removed: \-

Default Value: 120

Detail:
**Example:** Set xdr-tomb-raider-period to 500:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;xdr-tomb-raider-period=500"
```

---

#### `xdr-tomb-raider-threads`

`enterprise` `dynamic` `cloud`

Context: namespace

Description: The number of dedicated threads used by the xdr-tomb-raider to clear [`xdr_tombstones`](https://aerospike.com/docs/database/reference/metrics#namespace__xdr_tombstones).

Introduced: 5.0.0

Removed: \-

Default Value: 1

Detail:
**Example:** Set xdr-tomb-raider-threads to 4:

```plaintext
asinfo -v "set-config:context=namespace;id=namespaceName;xdr-tomb-raider-threads=4"
```

---

## Network

#### `access-address`

`static`

Context: network

Subcontext: service

Description: An access address is an IP address that is announced to clients and used by clients for connecting to the cluster.

If `access-address` is not specified, the bind address (through the [`address`](https://aerospike.com/docs/database/reference/config#network__address) config) is published to clients.

If `access-address` is not specified and the service `address` is set to `any`, then `access-address` lists all available IP addresses. Use `access-address` to specify one or more of the available IP addresses.

Multiple access addresses can be specified. IPv4, IPv6 and DNS names can be used to specify access addresses. DNS names are expanded to all IP addresses they resolve to, IPv4 (A DNS resource records) as well as IPv6 (AAAA DNS resource records). Set [`advertise-ipv6`](https://aerospike.com/docs/database/reference/config#service__advertise-ipv6) to `true` if using IPv6, otherwise, specifying an IPv6 address is ignored and reverts to the default described earlier.

The IP addresses that are specified under `access-address` must be available locally. See [`alternate-access-address`](https://aerospike.com/docs/database/reference/config#network__alternate-access-address) and [`tls-alternate-access-address`](https://aerospike.com/docs/database/reference/config#network__tls-alternate-access-address) for more information.

TLS equivalent are exposed through [`tls-access-address`](https://aerospike.com/docs/database/reference/config#network__tls-access-address) and [`tls-alternate-access-address`](https://aerospike.com/docs/database/reference/config#network__tls-alternate-access-address).

Introduced: \-

Removed: \-

Default Value: service address if specified or list of available IP addresses

Detail:
The info [`service-clear-std`](https://aerospike.com/docs/database/reference/info#service-clear-std) command will return a node’s access address(es) and the [`peers-clear-std`](https://aerospike.com/docs/database/reference/info#peers-clear-std) command will return a node’s peers access address(es) in a cluster. Multiple access addresses can be specified.

**Example:**

```asciidoc
service {

        ----

        access-address 10.0.0.104

        access-address 10.0.0.103

        ---

 }
```

---

#### `access-port`

`static`

Context: network

Subcontext: service

Description: Port number associated with [`access-address`](https://aerospike.com/docs/database/reference/config#network__access-address). If not specified, it defaults to the `port` value in the service stanza.

Introduced: \-

Removed: \-

Default Value: service port

---

#### `address`

`static`

Context: network

Subcontext: service, fabric, heartbeat

Description: IP address of an interface handling traffic for a network sub-context:

-   service deals with client and XDR traffic
-   fabric handles intra-cluster traffic (replica writes, migrations, duplicate resolution, clustering, exchange, migrations, and more)
-   heartbeat is a gossip protocol used for peer discovery.

Fabric and heartbeat should run on the same interface. One or more address lines may be used in the subcontexts of network.

-   Defaulting to `any` is deprecated. Define explicit addresses (IP or FQDN).
-   Defining an address in the heartbeat subcontext is deprecated. In a later version the heartbeat address will be inherited from the fabric subcontext.

Introduced: \-

Deprecated: default to \`any\` deprecated, removed \`network.info\` subcontext in 8.1.0

Removed: \-

Default Value: fabric, heartbeat sub-context inherit the address value from the service sub-context

---

#### `address`

`static`

Context: network

Subcontext: admin

Description: IP address at which the server listens (binds) for non‑secured (non‑TLS) admin connections.

Introduced: 8.1.0

Removed: \-

Default Value: \-

---

#### `disable-localhost`

`static`

Context: network

Subcontext: admin

Description: When set `true`, the service will not listen on localhost.

Introduced: 8.1.0

Removed: \-

Default Value: false

---

#### `port`

`static`

Context: network

Subcontext: admin

Description: Port that is not secured (non‑TLS) at which the server listens for admin client connections.

Introduced: 8.1.0

Removed: \-

Default Value: \-

---

#### `tls-address`

`static`

Context: network

Subcontext: admin

Description: IP address at which the server listens (binds) for secured (TLS) admin connections.

Introduced: 8.1.0

Removed: \-

Default Value: \-

---

#### `tls-authenticate-client`

`static`

Context: network

Subcontext: admin

Description: `false`: Only the client authenticates the server.

`any`: Two‑way (mutual) authentication—both client and server must be authenticated.

`user-defined`: Two‑way (mutual) authentication with additional subject validation.

Introduced: 8.1.0

Removed: \-

Default Value: false

---

#### `tls-name`

`static`

Context: network

Subcontext: admin

Description: Specifies which TLS parameters to use for the given context’s TLS connections.

Introduced: 8.1.0

Removed: \-

Default Value: \-

---

#### `tls-port`

`static`

Context: network

Subcontext: admin

Description: Port that is TLS enabled at which the server listens for admin client connections.

Introduced: 8.1.0

Removed: \-

Default Value: \-

---

#### `alternate-access-address`

`static`

Context: network

Subcontext: service

Description: Can be used to choose a specific IP address or DNS name that will be published as an alternate list for clients to connect (other than the one based on `address` and `access-address`). Prior to Database 5.0.0, XDR can make use of this by specifying [`dc-use-alternate-services true`](https://aerospike.com/docs/database/reference/config#xdr__dc-use-alternate-services). Starting with Database 5.0.0, use [`use-alternate-access-address`](https://aerospike.com/docs/database/reference/config#xdr__use-alternate-access-address).

Introduced: 3.10.0

Removed: \-

Default Value: \-

Detail:
Isolates clients based on public/private address or NATted environments like cloud deployments. Ability to specify a DNS name gives extra benefits.

Unlike its standard counterpart [`access-address`](https://aerospike.com/docs/database/reference/config#network__access-address), the IP address or DNS specified does not have to be local to the node.

---

#### `alternate-access-port`

`static`

Context: network

Subcontext: service

Description: Port number associated with [`alternate-access-address`](https://aerospike.com/docs/database/reference/config#network__alternate-access-address). If not specified, it defaults to the [`access-port`](https://aerospike.com/docs/database/reference/config#network__access-port) value.

Introduced: \-

Removed: \-

Default Value: access-port

---

#### `ca-file`

`enterprise` `static`

Context: network

Subcontext: tls

Description: Path to the CA file needed for mutual authentication. Only one of ca-file or [`ca-path`](https://aerospike.com/docs/database/reference/config#network__ca-path) is required. For XDR TLS connections, one of the 2 is mandatory. Defaults to the system’s default (/etc/ssl/certs/cacert.pem on Ubuntu) except for XDR where it should be set if needed.

Introduced: 3.15.0

Removed: \-

Default Value: \-

Detail:
**Example:**

```asciidoc
ca-file <path to file>
```

---

#### `ca-path`

`enterprise` `static`

Context: network

Subcontext: tls

Description: Path to the directory of the CA file for mutual authentication. Requires `openssl rehash <path to directory>` command be ran on the ca-path directory containing the CA certs. Only one of [`ca-file`](https://aerospike.com/docs/database/reference/config#network__ca-file) or ca-path configuration is required. For XDR TLS connections, one of the 2 is mandatory. Defaults to the system’s default (/etc/ssl/certs on Ubuntu) except for XDR where it should be set if needed.

Introduced: 3.15.0

Removed: \-

Default Value: \-

Detail:
**Example:**

```asciidoc
ca-path <path to directory>
```

---

#### `cert-blacklist`

`enterprise` `static`

Context: network

Subcontext: tls

Description: Path to the file containing rogue certificates serial numbers. Use this to revoke or blacklist rogue certificates. The file should contain the serial numbers of the certificates to be blacklisted, one per line. Since Database 7.1.0, blacklist file is periodically refreshed based on [`tls-refresh-period`](https://aerospike.com/docs/database/reference/config#service__tls-refresh-period) configuration value.

Prior to Database 7.1.0, only file-based `cert-blacklist` is supported. Since Database 7.1.0, file-based as well as external Secret Manager-based `cert-blacklist` is also supported.

Introduced: 3.15.0

Removed: \-

Default Value: \-

Detail:
**Example:**

File-based `cert-blacklist`

```asciidoc
cert-blacklist PATH TO FILE
```

external Secret Manager-based `cert-blacklist`

```asciidoc
cert-blacklist secrets:AerospikeSecrets:CertBlacklist
```

---

#### `cert-file`

`enterprise` `static`

Context: network

Subcontext: tls

Description: Path to the TLS certificate when TLS is enabled. Starting with Database 7.1.0, file-based as well as external Secret Manager-based TLS certificates are refreshed periodically using [`tls-refresh-period`](https://aerospike.com/docs/database/reference/config#service__tls-refresh-period) configuration. Prior to Database 7.1.0, only file-based certificates automatically reload on subsequent connections if the file itself changes.  
This parameter’s value must follow one of these formats. Prefixes `file:`, `env:`, `env-b64:`, `vault:`, and `secrets:` are literal strings.

-   `file:/path/to/cert` - Read from the filesystem (the `file:` prefix is optional).
-   `env:CERT` - Read from the named environment variable (Database 5.3.0+).
-   `vault:cert` - the named secret is read from [Vault](https://aerospike.com/docs/database/manage/security/vault) (Database 5.1.0+).
-   `secrets:AerospikeSecrets:CertFile` - fetched using [Aerospike Secret Agent](https://aerospike.com/docs/database/manage/security/secrets) (Database 6.4.0+).  
    .

Prior to Database 7.1.0, `cert-file` specified using Vault, environment variable, or Secret Agent is read when the server starts and is not re-read thereafter.

Introduced: 3.15.0

Removed: \-

Default Value: \-

Detail:
**Example:**

File based `cert-file`

```asciidoc
cert-file <path to file>
```

External Secret Manager-based `cert-file`

```asciidoc
cert-file secrets:AerospikeSecrets:CertFile
```

Fabric and Heartbeat TLS certificates prior to **4.7.0.5, 4.6.0.8, 4.5.3.10, 4.5.2.10, 4.5.1.15, 4.5.0.19** required a rolling restart to rotate expired certificates. ECDSA private keys and certificates rotations, and password-protected private keys rotations were also not supported until those same versions.

---

#### `channel-bulk-fds`

`static` `cloud`

Context: network

Subcontext: fabric

Description: Number of bulk channel sockets to open to each neighbor node. Twice this number of sockets per neighbor will be opened since the neighbor nodes will open the same number of sockets back to this node.

Introduced: 3.11.1.1

Removed: \-

Default Value: 2

Detail:
Minimum: 1  
  
Maximum: 128. Exceeding this maximum will prevent the server from starting.

---

#### `channel-bulk-recv-threads`

`dynamic` `cloud`

Context: network

Subcontext: fabric

Description: Number of threads processing intra-cluster messages arriving through the bulk channel. This channel is used for record migrations during rebalance.

Introduced: 3.11.1.1

Removed: \-

Default Value: 4

Detail:
**Example:** Set channel-bulk-recv-threads to 6 dynamically:

```plaintext
asinfo -v "set-config:context=network;fabric.channel-bulk-recv-threads=6"
```

Minimum: 1  
Maximum: 128. Exceeding this maximum will prevent the server from starting.

---

#### `channel-ctrl-fds`

`static` `cloud`

Context: network

Subcontext: fabric

Description: Number of control channel sockets to open to each neighbor node. Twice this number of sockets per neighbor will be opened since the neighbor nodes will open the same number of sockets back to this node.

Introduced: 3.11.1.1

Removed: \-

Default Value: 1

Detail:
Minimum: 1  
Maximum: 128. Exceeding this maximum will prevent the server from starting.

---

#### `channel-ctrl-recv-threads`

`dynamic` `cloud`

Context: network

Subcontext: fabric

Description: Number of threads processing intra-cluster messages arriving through the control channel. This channel distributes cluster membership change events as well as partition migration control messages.

Introduced: 3.11.1.1

Removed: \-

Default Value: 4

Detail:
**Example:** Set channel-ctrl-recv-threads dynamically to 6:

```plaintext
asinfo -v "set-config:context=network;fabric.channel-ctrl-recv-threads=6"
```

Minimum: 1  
Maximum: 128. Exceeding this maximum will prevent the server from starting.

---

#### `channel-meta-fds`

`static` `cloud`

Context: network

Subcontext: fabric

Description: Number of meta channel sockets to open to each neighbor node. Twice this number of sockets per neighbor will be opened since the neighbor nodes will open the same number of sockets back to this node.

Introduced: 3.11.1.1

Removed: \-

Default Value: 1

Detail:
Minimum: 1  
Maximum: 128. Exceeding this maximum will prevent the server from starting.

---

#### `channel-meta-recv-threads`

`dynamic` `cloud`

Context: network

Subcontext: fabric

Description: Number of threads processing intra-cluster messages arriving through the meta channel. This channel distributes System Meta Data (SMD) after cluster change events.

Introduced: 3.11.1.1

Removed: \-

Default Value: 4

Detail:
**Example:** Set channel-meta-recv-threads dynamically to 6:

```plaintext
asinfo -v "set-config:context=network;fabric.channel-meta-recv-threads=6"
```

Minimum: 1  
Maximum: 128. Exceeding this maximum will prevent the server from starting.

---

#### `channel-rw-fds`

`static` `cloud`

Context: network

Subcontext: fabric

Description: Number of read/write channel sockets to open to each neighbor node. Twice this number of sockets per neighbor will be opened since the neighbor nodes will open the same number of sockets back to this node.

Introduced: 3.11.1.1

Removed: \-

Default Value: 8

Detail:
Minimum: 1  
Maximum: 128. Exceeding this maximum will prevent the server from starting.

---

#### `channel-rw-recv-pools`

`static` `cloud`

Context: network

Subcontext: fabric

Description: Number of thread pools for the fabric rw (read/write) receive channel. Each thread pool has one epoll instance (Linux system call for scalable I/O event notification).

The configuration parameter [`channel-rw-recv-threads`](https://aerospike.com/docs/database/reference/config#network__channel-rw-recv-threads) must be a multiple of this setting (`channel-rw-recv-pools`).

Introduced: 5.1.0

Removed: \-

Default Value: 1

Detail:
For high throughput write workloads, increasing the number of [`channel-rw-recv-threads`](https://aerospike.com/docs/database/reference/config#network__channel-rw-recv-threads) can help, but you would also have to increase the number of thread pools (`channel-rw-recv-pools`) to prevent having all the fabric rw receive threads contend on a single epoll instance. A ratio of 16:1 (`channel-rw-recv-threads` : `channel-rw-recv-pools`) is a good starting point.

It may also be beneficial to adjust the [`channel-rw-fds`](https://aerospike.com/docs/database/reference/config#network__channel-rw-fds) and the [`send-threads`](https://aerospike.com/docs/database/reference/config#network__send-threads) to keep an 8:1 ratio with the `channel-rw-recv-pools`.

Proper benchmark testing is required for the best values for a given workload (as defined by throughput, objects type and size as well as general configuration such as compression and encryption — at rest as well as over the fabric channel). The send and receive buffer sizes (`tcp_rmem` and `tcp_wmem`) could also be tuned for extreme workloads.

---

#### `channel-rw-recv-threads`

`dynamic` `cloud`

Context: network

Subcontext: fabric

Description: Number of threads processing intra-cluster messages arriving through the rw (**r**ead/**w**rite) channel. This channel is used for replica writes, proxies, duplicate resolution, and various other intra-cluster single-record commands.

Minimum: 1.  
Maximum: 128. Exceeding this maximum will prevent the server from starting.

Starting with Database 5.1, configuration parameter [`channel-rw-recv-threads`](https://aerospike.com/docs/database/reference/config#network__channel-rw-recv-threads) must be a multiple of [`channel-rw-recv-pools`](https://aerospike.com/docs/database/reference/config#network__channel-rw-recv-pools).

Introduced: 3.11.1.1

Removed: \-

Default Value: 16

Detail:
**Example:** Set channel-rw-recv-threads to 24 dynamically:

```plaintext
asinfo -v "set-config:context=network;fabric.channel-rw-recv-threads=24"
```

---

#### `cipher-suite`

`enterprise` `static` `cloud`

Context: network

Subcontext: tls

Description: Ciphers to includes. This is not set by default on Aerospike and would revert to what the system uses, usually `ALL:!aNULL:!eNULL`.

Introduced: 3.15.0

Removed: \-

Default Value: \-

Detail:
**Example:**

```asciidoc
cipher-suite ALL:!COMPLEMENTOFDEFAULT:!eNULL
```

The parameter follows the same format as OpenSSL see [OpenSSL Documentation](http://www.openssl.org/docs/man1.1.0/man1/ciphers).

---

#### `connect-timeout-ms`

`dynamic` `cloud`

Context: network

Subcontext: heartbeat

Description: Node connection timeout within the cluster, in milliseconds. This timeout also applies to establishing and accepting TLS connections.

This value must be at least 50, and cannot be larger than one-third the product of `heartbeat.interval` and `heartbeat.timeout`

Introduced: 5.3.0

Removed: \-

Default Value: 500

Detail:
**Example:** Set `heartbeat.connect-timeout-ms` to 1200:

```plaintext
asinfo -v 'set-config:context=network;heartbeat.connect-timeout-ms=1200'
```

---

#### `disable-localhost`

`static`

Context: network

Subcontext: service

Description: When set `true`, the service will not listen on localhost.

Introduced: 5.6.0

Removed: \-

Default Value: false

---

#### `interval`

`dynamic` `cloud`

Context: network

Subcontext: heartbeat

Description: Interval in milliseconds between which heartbeats are sent. `interval` can be set to a minimum value of 50 and a maximum of 600000 (10 minutes).

Introduced: \-

Removed: \-

Default Value: 150

Detail:
**Example:** Set `heartbeat.interval` to 250:

```plaintext
asinfo -v 'set-config:context=network;heartbeat.interval=250'
```

Increasing `heartbeat.interval` will increase the tolerance of the cluster to minor network fluctuations, however, it will also mean that the cluster reacts more slowly to a genuine cluster event. In the event of a genuine cluster event, a higher `heartbeat.interval` time will mean that it takes longer for the cluster to acknowledge the node has left and, as a result, there may be a greater impact on the application. This setting will contribute to the calculated quantum interval. The quantum interval is 20% of the product of `heartbeat.timeout` and `heartbeat.interval`. The total time to detect a node failure on the client side would be: (heartbeat.interval x heartbeat.timeout) + 20% (heartbeat.interval x heartbeat.timeout) + Client\_tend\_interval. In general, though, given proper client policy settings for retries, clients would still be able to reach one of the nodes in the cluster which may then result in a proxy to the correct node.

---

#### `keepalive-enabled`

`static` `cloud`

Context: network

Subcontext: fabric

Description: Enables the nodes to send keep-alive messages to each other.

Introduced: 3.5.12

Removed: \-

Default Value: true

---

#### `keepalive-intvl`

`static` `cloud`

Context: network

Subcontext: fabric

Description: Interval in seconds between successive keep-alive packets.

Introduced: 3.5.12

Removed: \-

Default Value: 1

Detail:
If you set this keep-alive parameter to a non-positive number, the node does not override the corresponding Linux kernel system default for the parameter.

---

#### `keepalive-probes`

`static` `cloud`

Context: network

Subcontext: fabric

Description: Maximum number of keep-alive packets the node sends succession before declaring the socket dead.

Introduced: 3.5.12

Removed: \-

Default Value: 1

Detail:
If you set this keep-alive parameter to a non-positive number, the node does not override the corresponding Linux kernel system default for the parameter.

---

#### `keepalive-time`

`static` `cloud`

Context: network

Subcontext: fabric

Description: Time in seconds from the last user data packet sent on the socket before sending the first keep-alive packet.

Introduced: 3.5.12

Removed: \-

Default Value: 1

Detail:
If you set this keep-alive parameter to a non-positive number, the node does not override the corresponding Linux kernel system default for the parameter.

---

#### `key-file-password`

`enterprise` `static`

Context: network

Subcontext: tls

Description: Password for the [`key-file`](https://aerospike.com/docs/database/reference/config#network__key-file). This parameter’s value must follow one of these formats. Prefixes `file:`, `env:`, `env-b64:`, `vault:`, and `secrets:` are literal strings.

-   `file:/path/to/key-file-password` - Read from the filesystem (the `file:` prefix is optional).
-   `env:KEYPASS` - Read from the named environment variable (Database 5.3.0+).
-   `vault:key-file` - the named secret will be read from [Vault](https://aerospike.com/docs/database/manage/security/vault) (Database 5.1.0+).
-   `secrets:AerospikeSecrets:KeyFile` - fetched using [Aerospike Secret Agent](https://aerospike.com/docs/database/manage/security/secrets) (Database 6.4.0+).  
    .

This parameter is read when the server starts and is not re-read thereafter.

Introduced: 4.3.1

Removed: \-

Default Value: \-

Detail:
**Example:**

```asciidoc
key-file-password file:<path to keyfile pwd>
```

In Database 5.0.0 and 5.1, if an XDR datacenter is configured to use a TLS specification that includes [`key-file`](https://aerospike.com/docs/database/reference/config#network__key-file) _but does not include [`key-file-password`](https://aerospike.com/docs/database/reference/config#network__key-file-password)_ the system will crash. This problem is corrected by hotfixes to these versions available from the [Download](https://aerospike.com/download/) page.

---

#### `key-file`

`enterprise` `static`

Context: network

Subcontext: tls

Description: Path to the TLS key file when TLS is enabled. Starting with Database 7.1.0, file-based as well as external Secret Manager-based TLS certificates are refreshed periodically using [`tls-refresh-period`](https://aerospike.com/docs/database/reference/config#service__tls-refresh-period). Prior to Database 7.1.0, only file-based TLS certificates automatically reload on subsequent connections if the file itself changes.  
This parameter’s value must follow one of these formats. Prefixes `file:`, `env:`, `env-b64:`, `vault:`, and `secrets:` are literal strings.

-   `file:/path/to/key-file` - Read from the filesystem (the `file:` prefix is optional).
-   `env:KEYFILE` - Read from the named environment variable (Database 5.3.0+).
-   `vault:key-file` - the named secret will be read from [Vault](https://aerospike.com/docs/database/manage/security/vault) (Database 5.1.0+).
-   `secrets:AerospikeSecrets:KeyFile` - fetched using [Aerospike Secret Agent](https://aerospike.com/docs/database/manage/security/secrets) (Database 6.4.0+).  
    .

Prior to Database 7.1.0, `key-file` specified using Vault, environment variable, or Secret Agent is read when the server starts and is not re-read thereafter.

Introduced: 3.15.0

Removed: \-

Default Value: \-

Detail:
**Example:**

File based `key-file`

```asciidoc
key-file <path to key file>
```

External Secret manager based `key-file`

```asciidoc
key-file secrets:AerospikeSecrets:KeyFile
```

Fabric and Heartbeat TLS certificates prior to Database 4.7.0.5, 4.6.0.8, 4.5.3.10, 4.5.2.10, 4.5.1.15, 4.5.0.19 required a rolling restart to rotate expired certificates. ECDSA private keys and certificates rotations, and password-protected private keys rotations were also not supported until those same versions.

In Database 5.0.0 and 5.1, if an XDR datacenter is configured to use a TLS specification that includes [`key-file`](https://aerospike.com/docs/database/reference/config#network__key-file) _but does not include [`key-file-password`](https://aerospike.com/docs/database/reference/config#network__key-file-password)_ the system will crash. This problem is corrected by hotfixes to these versions available from the [Download](https://aerospike.com/download/) page.

---

#### `latency-max-ms`

`enterprise` `static` `cloud`

Context: network

Subcontext: fabric

Description: Maximum latency in milliseconds between nodes that the clustering system will tolerate. Used to derive the quantum interval, which helps to determine cluster reformation time after cluster event. Increasing this value can increase the amount of time it takes for a new cluster to form.  
  
This value is also used in the HLC (Hybrid Logical Clock) when determining if an event happened before or after another event. If two events occur less than this value apart, the ordering is indeterminate.  
  
The impact of this parameter on cluster reformation after cluster events is discussed in detail in the [What is the Quantum Interval](https://support.aerospike.com/s/article/FAQ-What-is-the-Quantum-Interval-and-how-does-it-affect-cluster-reformation-time) article. Changing this value may be appropriate in certain scenarios whereby intra-node network latency is necessarily high. Enterprise Licensees should consult with Aerospike Support before changing this configuration.

Introduced: 3.1.03.0

Removed: \-

Default Value: 5

Detail:
Allowable range is 0 to 1000.

---

#### `mesh-seed-address-port`

`static`

Context: network

Subcontext: heartbeat

Description: Mesh address (host-name or IP) and port info for seed server(s). These are other addresses from the cluster that Aerospike will bootstrap from. A new line is required for each additional boot strap. Applies only when mode is mesh.

Introduced: 3.3.19

Removed: \-

Default Value: false

Detail:
**Example:**

```asciidoc
mesh-seed-address-port 10.10.0.116 3002

mesh-seed-address-port aerospike_a_0 3002
```

When using fully qualified names in Database 4.3.1 and earlier, names that would not DNS resolve could cause clusters to split if the DNS server slows down and the name resolution takes longer to fail. A successful DNS resolution replaces the name with the IP address until the subsequent restart.

---

#### `mode`

`unanimous` `static`

Context: network

Subcontext: heartbeat

Description: In case of `multicast`, all cluster nodes must be in the same subnet. Multicast support is deprecated. Switch to `mesh`.”

Introduced: \-

Deprecated: 8.1.0

Removed: \-

Default Value: \-

Detail:
Example:

```asciidoc
mode multicast is deprecated
```

Changes to heartbeat mode require a cluster restart.

---

#### `mtu`

`enterprise` `dynamic` `cloud`

Context: network

Subcontext: heartbeat

Description: For the underlying network, returns the maximum transmission unit (MTU) detected by the heartbeat system.

Introduced: 3.9.1

Removed: \-

Default Value: 0

Detail:
Allowed value is any integer.

---

#### `multicast-group`

`static`

Context: network

Subcontext: heartbeat

Description: IP address for cluster-state heartbeat communication over multicast.

Introduced: 3.10.0

Removed: \-

Default Value: 239.1.99.222

---

#### `multicast-ttl`

`static` `cloud`

Context: network

Subcontext: heartbeat

Description: TTL for multicast packets.

Introduced: 3.10.0

Removed: \-

Default Value: 0

Detail:
IP multicast datagrams are sent with a time-to-live (TTL) of 1 by default. In Aerospike configuration “0” means use the default which is 1. Multicast datagrams with initial TTL 1 are restricted to the same subnet.

---

#### `pki-user-append-ou`

`static` `cloud`

Context: network

Subcontext: tls

Description: Defines how to derive the username for PKI authentication.

When `false`, the username comes from the CN (Common Name) field in the certificate. If the CN value is missing, authentication fails.

When `true`, the username is “CN-OU”, the CN value, followed by a dash, followed by the OU (Organizational Unit Name) value. If either of the CN value or OU value is missing, authentication fails.

“Defines whether, during PKI authentication, the server looks to the CN certificate field for the username, or derives it from a combination of the CN and OU fields.”

Introduced: 8.1.0

Removed: \-

Default Value: false

Detail:
**Example:**

```plaintext
network {

  tls CLUSTER-NAME {

     cert-file /home/user/cluster_chain.pem

     key-file /home/user/key.pem

     pki-user-append-ou true

  }

}
```

---

#### `port`

`static`

Context: network

Subcontext: fabric

Description: Port for inter-node communication within a cluster.

Introduced: \-

Removed: \-

Default Value: 3001 (in config)

---

#### `protocol`

`unanimous` `dynamic` `cloud`

Context: network

Subcontext: heartbeat

Description: Heartbeat protocol version to be used by cluster. Use `v3` or `none`. Protocol can only be changed on all nodes at once.

Introduced: \-

Removed: \-

Default Value: v3 (v. 3.14.0)

Detail:
-   `v3` = Improved cluster management and flexible cluster size, removes `paxos-max-cluster-size` dependency. Introduced in version 3.10.0.3.
    
-   `none` = Used **only** for dynamically changing protocol
    
    **Example:** Set `heartbeat.protocol` to v3.
    
    ```plaintext
    asinfo -v 'set-config:context=network;heartbeat.protocol=v3'
    ```

---

#### `protocols`

`enterprise` `static` `cloud`

Context: network

Subcontext: tls

Description: TLS protocol versions to include. The default is to only allow TLS protocol version 1.2.

Introduced: 3.15.0

Removed: \-

Default Value: TLSv1.2

Detail:
**Example:**

```asciidoc
protocols  -all,+TLSv1.2
```

In Database 4.6.0 the default protocols configuration parameter was changed from “-all,+TLSv1.2” to “TLSv1.2”.

---

#### `send-threads`

`static` `cloud`

Context: network

Subcontext: fabric

Description: Number of intra-node send threads to be used. The `send-threads` operate across all fabric channels.

Introduced: 3.11.1.1

Removed: \-

Default Value: 8

Detail:
Minimum: 1  
Maximum: 128. Exceeding this maximum will prevent the server from starting.

---

#### `timeout`

`dynamic` `cloud`

Context: network

Subcontext: heartbeat

Description: Number of missing heartbeats after which the remote node will be declared dead. Values lower than 3 are not allowed as this would potentially lead to very frequent timeout which could destabilize a cluster.

Introduced: \-

Removed: \-

Default Value: 10

Detail:
**Example:** Set `heartbeat.timeout` to 20:

```plaintext
asinfo -v 'set-config:context=network;heartbeat.timeout=20'
```

Increasing `heartbeat.timeout` will increase the tolerance of the cluster to minor network fluctuations, however, it will also mean that the cluster reacts more slowly to a genuine cluster event. In the event of a genuine cluster event, a higher `heartbeat.timeout` will mean that it takes longer for the cluster to acknowledge the node has left and, as a result, there may be a greater impact on the application. This setting will contribute to the calculated quantum interval. The quantum interval is 20% of the product of `heartbeat.timeout` and `heartbeat.interval`. The total time to detect a node failure on the client side would be: (heartbeat.interval x heartbeat.timeout) + 20% (heartbeat.interval x heartbeat.timeout) + Client\_tend\_interval. In general, though, given proper client policy settings for retries, clients would still be able to reach one of the nodes in the cluster which may then result in a proxy to the correct node.

---

#### `tls-access-address`

`enterprise` `static`

Context: network

Subcontext: service

Description: TLS equivalent of [`access-address`](https://aerospike.com/docs/database/reference/config#network__access-address).

Introduced: 3.1.01.0

Removed: \-

Default Value: any

---

#### `tls-access-port`

`enterprise` `static`

Context: network

Subcontext: service

Description: Transport Layer Security (TLS) equivalent of [`access-port`](https://aerospike.com/docs/database/reference/config#network__access-port).

Introduced: \-

Removed: \-

Default Value: tls-port

---

#### `tls-address`

`enterprise` `static`

Context: network

Subcontext: service,heartbeat,fabric

Description: Bind address for TLS, the IP address at which the server listens for client connections, heartbeat connections or fabric connections (based on the subcontext this is set at). Similar to address when not using TLS. Will default to any if not set.

Introduced: 3.1.01.0

Removed: \-

Default Value: \-

---

#### `tls-alternate-access-address`

`enterprise` `static`

Context: network

Subcontext: service

Description: TLS equivalent of [`alternate-access-address`](https://aerospike.com/docs/database/reference/config#network__alternate-access-address).

Introduced: 3.1.01.0

Removed: \-

Default Value: \-

Detail:
Unlike its standard counterpart [`tls-access-address`](https://aerospike.com/docs/database/reference/config#network__tls-access-address), does not have to be local to the node.

---

#### `tls-authenticate-client`

`enterprise` `static`

Context: network

Subcontext: service

Description: The TLS authentication mode you want to run the server with in regards to the service (Client connections). See the [TLS Configuration Manual](https://aerospike.com/docs/database/manage/network/tls) for further details. Multiple `tls-authenticate-client` directives can be specified.

Introduced: 3.15.0

Removed: \-

Default Value: any

Detail:
Options:  
  
There are three modes you can have TLS configured, standard authentication (server only), mutual authentication (TLS client and TLS server), mutual authentication with subject validation. If not specified will default to `any` (mutual authentication without subject validation).

-   `false`: Use this for only client authenticating the server.
-   `any`: Use this is for a two way (mutual) authentication, both client and server need to be authenticated. Also check configs `ca-file` and `ca-path` when set to this mode.
-   user-defined: Use this for two way (mutual) authentication along with subject validation. This would be the TLS name a cluster node would expect clients to present on incoming connections.  
      
    Note: false and any are incompatible with each other and incompatible with a subject name, so if false or any is used, then there can only be one `tls-authenticate-client` directive.  
    Note: There isn’t any `tls-authenticate-client` for heartbeat and fabric. They always validate the subject name in their peer’s certificate and expect it to match the TLS name.

**Example:**

```asciidoc
service {

    <...>

    tls-authenticate-client remote-xdr-dc.aerospike.com

    tls-authenticate-client local-clients.aerospike.com

    <...>

}
```

---

#### `tls-mesh-seed-address-port`

`enterprise` `static`

Context: network

Subcontext: heartbeat

Description: TLS mesh address (host-name or IP) and port info for seed server(s). These are other addresses from the cluster that Aerospike will bootstrap from. A new line is required for each additional boot strap. Applies only when mode is mesh.

Introduced: 3.15.0

Removed: \-

Default Value: false

Detail:
**Example:**

```asciidoc
tls-mesh-seed-address-port 10.10.0.116 3012

tls-mesh-seed-address-port aerospike_a_0 3022
```

---

#### `tls-name`

`enterprise` `static`

Context: network

Subcontext: service,heartbeat,fabric

Description: Specifies which TLS parameters to use for the given context TLS connections. The TLS parameters are configured under the matching [`tls`](https://aerospike.com/docs/database/reference/config#network__tls) sub-stanza. This also implicitly specifies the TLS name the node will present on incoming client connections. See [TLS Name Clarification](https://aerospike.com/docs/database/learn/security/tls#tls-name-clarification) for details.

Introduced: 3.1.01.0

Removed: \-

Default Value: \-

---

#### `tls-port`

`enterprise` `static`

Context: network

Subcontext: service,heartbeat,fabric

Description: Port that is TLS enabled at which the server listens for client connections, heartbeat connections or fabric connections based on the subcontext this is set to.

Introduced: 3.1.01.0

Removed: \-

Default Value: \-

---

#### `tls`

`enterprise` `static` `cloud`

Context: network

Subcontext: tls

Description: Definition of TLS parameters for a given [`tls-name`](https://aerospike.com/docs/database/reference/config#network__tls-name). Can be `<cluster-name>` (literally), `<hostname>` (literally) or user defined. See the [TLS Configuration Manual](https://aerospike.com/docs/database/manage/network/tls) for further details.

Introduced: 3.15.0

Removed: \-

Default Value: \-

Detail:
**Example:**

```asciidoc
tls <cluster-name> {

       cert-file path-to-cert-file

       key-file path-to-key-file

}
```

---

## Security

#### `default-password-file`

`enterprise` `static`

Context: security

Description: A path or an optional prefix, such as `env:` or `secrets:` to specify where to fetch the initial password for the default `admin` user. If not configured, the old default password “admin” is used.

Introduced: 7.1.0

Removed: \-

Default Value: null

---

#### `disable-tls`

`enterprise` `static` `cloud`

Context: security

Subcontext: ldap

Description: Whether or not to disable the use of TLS for LDAP server connections

Introduced: 4.1.0

Removed: \-

Default Value: false

---

#### `enable-ldap`

`enterprise` `static`

Context: security

Description: Enables LDAP. See the [LDAP Configuration](https://aerospike.com/docs/database/manage/security/ldap) documentation for further details.  
Requires the `asdb-ldap` feature-key to be enabled in the [`feature-key-file`](https://aerospike.com/docs/database/reference/config#service__feature-key-file).  
  
As of Database 5.7.0, this item is removed, and LDAP is enabled by the presence of an `ldap` section within the `security` section of the configuration file.

Introduced: 4.1.0

Removed: 5.7.0

Default Value: false

---

#### `enable-quotas`

`enterprise` `static` `cloud`

Context: security

Description: Enables read and write rate quotas to limit transaction rates. Quotas can be added to roles, and users assigned such roles are restricted according to the associated quotas.  
When `enable-quotas` is `true`, read and write transaction per second (TPS) rates and scan record per second (RPS) rates are tracked for all users, even users with no quotas, and can be displayed with the “show users statistics” command in asadm which was added in tools package 8.4.0.

Introduced: 5.6.0

Removed: \-

Default Value: false

---

#### `enable-security`

`enterprise` `static`

Context: security

Description: Enables Access Control (ACL). See [Configuring Access Control in EE and FE](https://aerospike.com/docs/database/manage/security/rbac) for further details.

Database 4.6.0.4 and later, 4.5.3.6, 4.5.2.6, 4.5.1.11 and 4.5.0.15 support enabling ACL through a rolling restart, allowing environments running on the latest Client Libraries (supporting mixed security modes) to turn on ACL without downtime. The AER-6099 improvement was made to allow the System Metadata (SMD) sub-system to support mixed security modes on the server side.  
  
Starting with Database 5.7, this item is removed, and ACL is enabled by the presence of a `security` section in the configuration file.

Introduced: \-

Removed: 5.7.0

Default Value: false

Detail:
For Aerospike Enterprise Editions not having the AER-6099 improvement, enabling ACL requires a cluster shut down.

When configuring enable-security to true with Database 4.6.0 or later there are some incompatible Aerospike Clients. See [Overview of Access Control with LDAP and PKI](https://aerospike.com/docs/database/manage/security/rbac)  for compatible Aerospike client versions.

When configuring enable-security to true with Cross-Datacenter Replication (XDR) a cluster installed with Database 4.1.0.1 to 4.3.0.6 **cannot ship to** an Aerospike Database 4.6.0 or later. The simplest workaround is to avoid using those incompatible with Database 4.1.0.1 to 4.3.0.6. See the [ALC/XDR Knowledge Base article](https://support.aerospike.com/s/article/Internal-user-warning-returned-when-using-an-Access-Control-List-ACL-with-Cross-Datacenter-Replication-XDR-non-compatible-Aerospike-Server-versions-sending-both-internal-and-external-authentication-mode) for more information.

---

#### `ldap-login-threads`

`enterprise` `static`

Context: security

Description: Number of threads to use for LDAP logins.

Introduced: 4.1.0.1

Removed: 5.7.0

Default Value: 8

Detail:
Allowable range is 1 to 64. This parameter was renamed to [`login-threads`](https://aerospike.com/docs/database/reference/config#security__login-threads) and moved from the main security context to the ldap subcontext in Database 5.7.0.

---

#### `local0`

`enterprise` `unanimous` `static`

Context: security

Subcontext: syslog

Description: Write to “local0” facility as well as to default syslog file. You can define local0 in /etc/rsyslog.conf.

Introduced: \-

Removed: 6.3.0

Default Value: \-

---

#### `login-threads`

`enterprise` `static` `cloud`

Context: security

Subcontext: ldap

Description: Number of threads to use for LDAP logins.

Introduced: 5.7.0

Removed: \-

Default Value: 8

Detail:
Allowable range is 1 to 64. This parameter was renamed from [`ldap-login-threads`](https://aerospike.com/docs/database/reference/config#security__ldap-login-threads) and moved from the main security context to the ldap subcontext in database 5.7.

---

#### `polling-period`

`enterprise` `dynamic` `cloud`

Context: security

Subcontext: ldap

Description: How frequently (in seconds) to query the LDAP server for user group membership information. Allowable range is 0 to 86400 (24 hours). A value of 0 means do not poll.

Introduced: 4.1.0

Removed: \-

Default Value: 300 (5 minutes)

---

#### `privilege-refresh-period`

`enterprise` `dynamic` `cloud`

Context: security

Description: Frequency in seconds with which the node verifies permissions for active client connections.

Introduced: \-

Removed: \-

Default Value: 300

Detail:
**Example:** Set privilege-refresh-period to 200 dynamically:

```plaintext
asinfo -v "set-config:context=security;privilege-refresh-period=200"
```

---

#### `query-base-dn`

`enterprise` `required` `static` `cloud`

Context: security

Subcontext: ldap

Description: Distinguished name of the LDAP directory entry at which to begin the search when querying for a user’s group membership information.

Introduced: 4.1.0

Removed: \-

Default Value: \-

Detail:
Certain characters in the value of this parameter must be escaped. See [Parameters whose values must be escaped](https://aerospike.com/docs/database/manage/security/ldap#parameters-whose-values-must-be-escaped).

---

#### `query-user-dn`

`enterprise` `static` `cloud`

Context: security

Subcontext: ldap

Description: Distinguished name of the user designated for user group membership queries.

Introduced: 4.1.0

Removed: \-

Default Value: \-

Detail:
Certain characters in the value of this parameter must be escaped. See [Parameters whose values must be escaped](https://aerospike.com/docs/database/manage/security/ldap#parameters-whose-values-must-be-escaped).

---

#### `query-user-password-file`

`enterprise` `static`

Context: security

Subcontext: ldap

Description: Clear text password of the user specified for user group membership queries.  
This parameter’s value must follow one of these formats. Prefixes `file:`, `env:`, `env-b64:`, `vault:`, and `secrets:` are literal strings.

-   `file:/path/to/ldap-query-password` - Read from the filesystem (the `file:` prefix is optional).
-   `env:LDAPQPASS` - Read from the named environment variable (Database 5.3.0+).
-   `vault:ldap-query-password` - the named secret will be read from [Vault](https://aerospike.com/docs/database/manage/security/vault) (Database 5.1.0+).
-   `secrets:AerospikeSecrets:LDAPQueryPass` - fetched using [Aerospike Secret Agent](https://aerospike.com/docs/database/manage/security/secrets) (Database 6.4.0+).  
    .

Introduced: 4.1.0

Removed: \-

Default Value: \-

Detail:
As of Database 5.1.0, the password contents are re-read whenever the password is used.

In Database 5.1.0.3, this configuration parameter is dynamic and setting it dynamically may cause a crash.

---

#### `report-authentication`

`enterprise` `dynamic` `cloud`

Context: security

Subcontext: log

Description: Set to true to report successful authentications in aerospike.log.  
This parameter is dynamic starting with Database 5.6.

Introduced: \-

Removed: \-

Default Value: \-

Detail:
**Example:** Set the parameter dynamically:

```plaintext
asinfo -v "set-config:context=security;log.report-authentication=true"
```

---

#### `report-data-op-role`

`enterprise` `dynamic` `cloud`

Context: security

Subcontext: log

Description: Set this to report on data transactions for all users having a given role. Report transactions in aerospike.log.

Introduced: 5.6.0

Removed: \-

Default Value: \-

Detail:
**Example:** Enable reporting of data operations by all users having the ‘billing’ role:

```asciidoc
report-data-op-role billing
```

Dynamically disable reporting of data operations to aerospike.log by all users having the ‘billing’ role:

```plaintext
asinfo -v "set-config:context=security;log.report-data-op=false;role=billing"
```

Setting this for roles with medium and higher throughput could significantly degrade overall performance and cause flooding in the logs.

---

#### `report-data-op-user`

`enterprise` `dynamic` `cloud`

Context: security

Subcontext: log

Description: Set this to report on data transactions for a given user. Report transactions in aerospike.log.

Introduced: 5.6.0

Removed: \-

Default Value: \-

Detail:
**Example:** Enable reporting of data operations by user ‘charlie’:

```asciidoc
report-data-op-user charlie
```

Dynamically enable reporting of data operations by user ‘fred’:

```plaintext
asinfo -v "set-config:context=security;log.report-data-op=true;user=fred"
```

Setting this for users with medium and higher throughput could significantly degrade overall performance and cause flooding in the logs.

---

#### `report-data-op`

`enterprise` `dynamic` `cloud`

Context: security

Subcontext: log

Description: Set this to report on data transactions for a namespace (and optionally a set). Report transactions in aerospike.log.  
This parameter is dynamic starting with Database 5.6.

Introduced: \-

Removed: \-

Default Value: \-

Detail:
**Example:**

```asciidoc
report-data-op {namespace} {set}
```

Dynamically enable reporting of data operations to aerospike.log for set ‘setA’ in namespace ‘test’:

```plaintext
asinfo -v "set-config:context=security;log.report-data-op=true;namespace=test;set=setA"
```

Setting this for namespaces or sets with medium and higher throughput could significantly degrade overall performance and cause flooding in the logs.

---

#### `report-sys-admin`

`enterprise` `dynamic` `cloud`

Context: security

Subcontext: log

Description: Set to true to report systems administration operations in aerospike.log.  
This parameter is dynamic starting with Database 5.6.

Introduced: \-

Removed: \-

Default Value: \-

Detail:
**Example:** Set the parameter dynamically:

```plaintext
asinfo -v "set-config:context=security;log.report-sys-admin=true"
```

---

#### `report-user-admin`

`enterprise` `dynamic` `cloud`

Context: security

Subcontext: log

Description: Set to true to report successful user administration operations in aerospike.log.  
This parameter is dynamic starting with Database 5.6.

Introduced: \-

Removed: \-

Default Value: \-

Detail:
**Example:** Set the parameter dynamically:

```plaintext
asinfo -v "set-config:context=security;log.report-user-admin=true"
```

---

#### `report-violation`

`enterprise` `dynamic` `cloud`

Context: security

Subcontext: log

Description: Set to true to report security violations in aerospike.log.  
This parameter is dynamic starting with Database 5.6.

Introduced: \-

Removed: \-

Default Value: \-

Detail:
**Example:** Set the parameter dynamically:

```plaintext
asinfo -v "set-config:context=security;log.report-violation=true"
```

---

#### `role-query-base-dn`

`enterprise` `static` `cloud`

Context: security

Subcontext: ldap

Description: If specified uses this value as the base dn when performing the role queries.

Introduced: 4.1.0

Removed: \-

Default Value: query-base-dn value is used.

Detail:
Certain characters in the value of this parameter must be escaped. See [Parameters whose values must be escaped](https://aerospike.com/docs/database/manage/security/ldap#parameters-whose-values-must-be-escaped).

---

#### `role-query-pattern`

`enterprise` `required` `static` `cloud`

Context: security

Subcontext: ldap

Description: Format for the search filter to use when querying for a user’s group membership information. The substitutions for username, `${un}`, and distinguished name, `${dn}` will be replaced by the actual username and the actual user’s full distinguished name when constructing the search filter. If needed, multiple role-query-pattern strings can be specified separately and each will be tried in order when querying for a user’s information

Introduced: 4.1.0

Removed: \-

Default Value: \-

---

#### `role-query-search-ou`

`enterprise` `static` `cloud`

Context: security

Subcontext: ldap

Description: Whether to look for a user’s group membership information in the organizational unit entries of the user’s LDAP distinguished name

Introduced: 4.1.0

Removed: \-

Default Value: false

---

#### `server`

`enterprise` `required` `static` `cloud`

Context: security

Subcontext: ldap

Description: Name of the LDAP server to use. Multiple servers can be specified using a comma-delimited string without white-space.

Introduced: 4.1.0

Removed: \-

Default Value: \-

---

#### `session-ttl`

`enterprise` `dynamic`

Context: security

Description: The lifetime, in seconds, of an access token. A TCP connection attempt fails if using an expired token, and the client must log in again to get a fresh token. The allowable TTL range is 120 (2 minutes) to 864000 (10 days). As part of the login response, the server sends a session token expiration timestamp to the client at login. This timestamp is shortened on the clients by 60 seconds (session-ttl - 60s). The 60-second shorter timestamp ensures that the clients will log in again to refresh their token and avoid getting too close to the time the server session expires.

This parameter was moved from the `ldap` subcontext into the main `security` context in Database 5.7.0.

Introduced: 4.1.0

Removed: \-

Default Value: 86400

---

#### `syslog-local`

`enterprise` `static`

Context: security

Subcontext: syslog

Description: Local syslog file to log to.

Introduced: 3.3.13

Removed: 6.3.0

Default Value: 1

Detail:
The default value is -1, which means no logging.  
  
Allowable range is 0 to 7.  
  
The precise use of the syslog facilities local0 through local7 depends on your syslog implementation.

---

#### `tls-ca-file`

`enterprise` `required` `static`

Context: security

Subcontext: ldap

Description: Path to the CA certificate file used for validating TLS connections to the LDAP server. Includes filename, e.g. /path/to/CA/cert/filename.

Introduced: 4.1.0

Removed: \-

Default Value: \-

Detail:
May not be specified if `disable-tls` is set to `true`.

---

#### `token-hash-method`

`enterprise` `static` `cloud`

Context: security

Subcontext: ldap

Description: Hash algorithm to use when generating the HMAC for access tokens. Currently supported algorithms are sha-256 and sha-512.

Introduced: 4.1.0

Removed: \-

Default Value: sha-256

---

#### `tps-weight`

`enterprise` `dynamic` `cloud`

Context: security

Description: A number indicating how much smoothing to do when maintaining transactions per second (tps) values for enforcing quotas. Smoothing makes the system less responsive to brief spikes in transaction rates, so that the more smoothing is used, the less likely it is that a brief spike in transactions greater than a user’s quota will result in a violation. The allowable range is 2 (least smoothing) to 20 (most smoothing).

Introduced: 5.6.0

Removed: \-

Default Value: 2

Detail:
The tps rates are computed every second as exponential moving averages, and a tps-weight of N means that the previous tps value is given (N-1) times the weight of the observed tps over the most recent second when performing the computation. The computation looks like:  
  
`tps = (((tps-weight - 1) * tps) + transactions_during_last_second) / tps-weight`  
  
So for example, with a tps-weight of 5, the computation would be:  
  
`tps = ((4 * tps) + transactions_during_last_second) / 5`  

**Example:** Set tps-weight to 8 dynamically:

```plaintext
asinfo -v "set-config:context=security;tps-weight=8"
```

---

#### `user-dn-pattern`

`enterprise` `static` `cloud`

Context: security

Subcontext: ldap

Description: Format for the distinguished name of the LDAP directory entry to use when binding to the LDAP server for user authentication. `${un}` should be placed in this string to specify where the user ID is inserted when constructing the distinguished name.

Introduced: 4.1.0

Removed: \-

Default Value: \-

Detail:
Either this option or `user-query-pattern` is required. Certain characters in the value of this parameter must be escaped. See [Parameters whose values must be escaped](https://aerospike.com/docs/database/manage/security/ldap#parameters-whose-values-must-be-escaped).

---

#### `user-query-pattern`

`enterprise` `static` `cloud`

Context: security

Subcontext: ldap

Description: Format for the search filter to use when querying for a user’s distinguished name.`${un}` should be placed in this string to specify where the user ID is inserted when constructing the distinguished name.

Introduced: 4.1.0

Removed: \-

Default Value: \-

Detail:
Either this option or `user-dn-pattern` is required. As of Database 5.1.0, Aerospike server escapes certain illegal characters in the user DN returned by the LDAP server before making role queries for the user. Previous versions would fail querying the LDAP server if such characters are present. The characters that are escaped are as follows:

-   \*
-   (
-   )
-   \\
-   /
-   space

---

## Service

#### `advertise-ipv6`

`enterprise` `dynamic`

Context: service

Description: Requires heartbeat v3. Set to true in order enable IPv6.

Introduced: 3.10.0

Removed: \-

Default Value: false

---

#### `auto-pin`

`static` `cloud`

Context: service

Description: This configuration controls the different options for CPU pinning. When using this configuration prior to Database 4.7.0, neither [`service-threads`](https://aerospike.com/docs/database/reference/config#service__service-threads), nor `transaction-queues` may be configured in the configuration file; both will default to the number of CPUs. With Aerospike 4.7.0+, [`service-threads`](https://aerospike.com/docs/database/reference/config#service__service-threads) can be configured, but must be a multiple of the number of CPUs, if this configuration is in effect. Possible values are:

-   `none` - relying on Linux’s irqbalance.
-   `cpu` - CPU pinning - Aerospike controls the interrupt affinity of all NIC queue interrupts.
-   `numa` - CPU and NUMA pinning - restrict memory and CPU usage of `asd` to a single NUMA node.
-   `adq` - application device queue pinning (deprecated in Database 8.1.0)

Introduced: 3.1.02.0

Removed: \-

Default Value: none

Detail:
`cpu` and `numa` require Linux kernel 3.19+. Default for Ubuntu18.04+ and Debian 9+, but not CentOS 7 (3.10). If necessary, the Linux kernel can be upgraded. When moving away from any auto-pinning, a reboot is required to restore the system defaults for interrupts. When setting `auto-pin` to `cpu`, prior to Database 4.7.0 don’t allow `transaction-queues` and `service-threads` to be set in the configuration file; both will be forced to the number of CPUs - which is also the default in Aerospike versions 3.12.0+. Database 4.7.0 and later allows setting `service-threads`, but require the configured number to be a multiple of the number of CPUs. Contact Aerospike Support for recommendations and benchmark details prior to using these configurations.

The network interface hardware should support MSI. MSI sends interrupts from a peripheral device (e.g., a NIC) to the CPU using the PCI bus. Older hardware had dedicated lines for that, so any data exchange between the CPU and the device went using the PCI bus and interrupts were handled using a separate path, out of band. But in recent days everything goes through the PCI bus. Network interfaces not supporting MSI would assert with the following:

```plaintext
FAILED ASSERTION (hardware): (hardware.c:1087) interface eth0 does not support MSIs
```

It is also necessary for the ratio of NIC queues to CPU cores be greater than 1/4. The following message would otherwise be logged on the console and the server would not start:

```plaintext
WARNING (hardware): (hardware.c:1605) eth0 has very few NIC queues; only 8 out of 32 CPUs handle(s) NIC interrupts
```

---

#### `batch-index-threads`

`dynamic` `cloud`

Context: service

Description: Number of batch index response worker threads. This is set by default to the number of CPU cores available. Each thread has its own queue. These threads only handle sending back batch response buffers to the client using sockets. Setting this parameter to 0 disables batch commands. Config file value range: 1-256 (a value of 0 can be set dynamically).

Introduced: 3.6.0

Removed: \-

Default Value: #cpu

Detail:
**Example:** Set batch-index-threads to 16 dynamically:

```plaintext
asinfo -v "set-config:context=service;batch-index-threads=16"
```

---

#### `batch-max-buffers-per-queue`

`dynamic` `cloud`

Context: service

Description: Number of 128 KiB response buffers allowed in each batch index queue before it is marked as full. A batch index queue (one per [`batch-index-threads`](https://aerospike.com/docs/database/reference/config#service__batch-index-threads)) can have more than `batch-max-buffers-per-queue` buffers but it will not receive any new batch until it gets less than that number. When all queues are greater than the `batch-max-buffers-per-queue` new batch requests are rejected and an error will be logged on the server: _Failed to find active batch queue that is not full_.

Introduced: 3.6.0

Removed: \-

Default Value: 255

Detail:
**Example:** Set batch-max-buffers-per-queue to 512 dynamically:

```plaintext
asinfo -v "set-config:context=service;batch-max-buffers-per-queue=512"
```

---

#### `batch-max-requests`

`dynamic` `cloud`

Context: service

Description: Max number of keys allowed per node. Limits the number of sub-requests per batch transaction. The default value of 0 means there is no limit.

Removed in database 6.4.0. Re-introduced in database 7.1.0.

Introduced: 7.1.0

Default Value: 0

Detail:
**Example:** Set batch-max-requests to 6000 dynamically:

```plaintext
asinfo -v "set-config:context=service;batch-max-requests=6000"
```

---

#### `batch-max-unused-buffers`

`dynamic` `cloud`

Context: service

Description: Max number of 128 KiB response buffers allowed in the unused buffer pool for reuse by any response thread. If the limit is reached, completed buffers will be destroyed at the end of the batch request. For large batch workloads, it may be advisable to increase this configuration parameter to avoid unnecessary destruction and recreation of buffers, which would impact CPU load.

Introduced: 3.6.0

Removed: \-

Default Value: 256

Detail:
**Example:** Set batch-max-unused-buffers to 512 dynamically:

```plaintext
asinfo -v "set-config:context=service;batch-max-unused-buffers=512"
```

---

#### `batch-without-digests`

`dynamic`

Context: service

Description: If set to true, digests are not included in batch responses.

Starting with Database 5.7.0, the default value is `true`. In earlier versions the default value is false.

Introduced: 4.9.0

Removed: 6.0.0

Default Value: true

Detail:
**Example:** Dynamically set batch-without-digests to false:

```plaintext
asinfo -v "set-config:context=service;batch-without-digests=false"
```

To use `batch-without-digests`, the minimum client versions required are as follows:

-   Java client version 4.4.5
-   C client version 4.6.6
-   C# client version 3.9.0
-   PHP client version 7.4.2.
-   Python client version 3.9.0.
-   Node.js client version 3.12.0

---

#### `cluster-name`

`required` `unanimous` `dynamic`

Context: service

Description: Mandatory in Database 7.0.0 and later. Maximum 63 characters. Node can only join a cluster with a matching `cluster-name`. Clients must provide matching cluster name. Configuration file of a new node must specify a non-null cluster name or node will not start.

An application or client must provide the IP address of the seed node to connect. IP addresses in the cloud are assigned dynamically when instances are created. Customers running multiple, separate Aerospike clusters in the cloud can ensure secondary validation that their application is connecting to the intended cluster by optionally using cluster name in their client policy.

Use `asinfo` to dynamically change the cluster name on a specific node, or `asadm` to dynamically change the cluster name on all nodes simultaneously.

While this parameter is unanimous, it does not require a recluster command or cluster restart to take effect. It is implemented by the continual heartbeat exchange.

Introduced: 3.10.0 (heartbeat v3)

Removed: \-

Default Value: null

Detail:
**Examples:**

-   Dynamically set `cluster-name` to _payments_ on the current node:

```plaintext
asinfo -v "set-config:context=service;cluster-name=payments"
```

-   Dynamically set `cluster-name`to _payments_ on all nodes simultaneously:

```plaintext
Admin+> manage config service param cluster-name to payments
```

---

#### `debug-allocations`

`static` `cloud`

Context: service

Description: Options for debugging memory allocations on the server.

Introduced: 3.1.04.0

Removed: \-

Default Value: false

Detail:
Starting with Database 7.0.0, the options are `false` (default) or `true`.  
  
Prior to Database 7.0.0

-   `none` - Feature not enabled (default).
-   `transient` - Feature enabled only for transient allocations - ‘overhead’ memory that is not record data or metadata.
-   `persistent` - Feature enabled only for persistent allocations - memory that is record data or metadata.
-   `all` - Feature enabled for all allocations.

When `debug-allocations` is enabled, the server will assert on detection of overwrites and (some) double frees. Also, each tracked allocation will incur a cost of 4 extra bytes.

For more complete debugging of double frees, also enable [`indent-allocations`](https://aerospike.com/docs/database/reference/config#service__indent-allocations).

When running with `debug-allocations` enabled for an extended time period (typically many months, though possibly sooner if using scans frequently with Database 4.7.0 or later), internal memory tracking resources can eventually become exhausted. With older Aerospike versions (Database 3.14.0 through 4.4; 4.5.0 versions prior to 4.5.0.19; 4.5.1 versions prior to 4.5.1.15; 4.5.2 versions prior to 4.5.2.10; 4.5.3 versions prior to 4.5.3.10; 4.6 versions prior to 4.6.0.8; 4.7 versions prior to 4.7.0.5), this condition leads to a crash. With later Aerospike versions (4.5.0 versions 4.5.0.19 or later; 4.5.1 versions 4.5.1.15 or later; 4.5.2 versions 4.5.2.10 or later; 4.5.3 versions 4.5.3.10 or later; 4.6 versions 4.6.0.8 or later; 4.7 versions 4.7.0.5 or later), this condition simply results in the inability to detect any further memory leaks.

---

#### `disable-udf-execution`

`static` `cloud`

Context: service

Description: Completely disallow the execution of User-Defined Functions (UDFs).

Introduced: 4.5.3.21

Removed: \-

Default Value: false

Detail:
**Example:** Disable UDF execution:

```asciidoc
service {

  ...

  disable-udf-execution true

  ...

}
```

Available starting with the following versions: 5.1.0.6, 5.0.0.7, 4.9.0.10, 4.8.0.13, 4.7.0.17, 4.6.0.19, 4.5.3.21.

---

#### `downgrading`

`enterprise` `dynamic`

Context: service

Description: Used in conjunction with downgrades from Database 5.2 or later (where XDR bin shipping has been used) to pre-5.2, or from Database 5.4 (where XDR bin convergence has been used) to 5.3 or 5.2, or from Database 5.5 or later (where XDR bin convergence has been used) to 5.4 or 5.3 or 5.2. When set `true` before downgrading, ensures record compatibility when sending records from nodes with the later server version to nodes with the older version. This parameter can only be set dynamically.

Introduced: 5.4.0.3, 5.3.0.8, 5.2.0.17

Removed: 7.0.0

Default Value: \-

Detail:
**Example:** Set to `true`:

```plaintext
asinfo -v "set-config:context=service;downgrading=true"
```

---

#### `enable-benchmarks-fabric`

`dynamic` `cloud`

Context: service

Description: Enable histograms for fabric. See the [Histograms from Aerospike Logs](https://aerospike.com/docs/database/observe/latency) page for details.

Introduced: 3.9.0

Removed: \-

Default Value: false

Detail:
Here is the list of configuration enabled histograms:  

-   [`enable-benchmarks-batch-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-batch-sub)
-   [`enable-benchmarks-fabric`](https://aerospike.com/docs/database/reference/config#service__enable-benchmarks-fabric)
-   [`enable-benchmarks-ops-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-ops-sub)
-   [`enable-benchmarks-read`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-read)
-   [`enable-benchmarks-storage`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-storage)
-   [`enable-benchmarks-udf`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-udf)
-   [`enable-benchmarks-udf-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-udf-sub)
-   [`enable-benchmarks-write`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-write)
-   [`enable-hist-info`](https://aerospike.com/docs/database/reference/config#service__enable-hist-info)
-   [`enable-hist-proxy`](https://aerospike.com/docs/database/reference/config#namespace__enable-hist-proxy)
-   [`sindex-histogram`](https://aerospike.com/docs/database/observe/latency)

**Example:** Set `enable-benchmarks-fabric` to true:

```plaintext
asinfo -v 'set-config:context=service;enable-benchmarks-fabric=true'
```

---

#### `enable-health-check`

`dynamic` `cloud`

Context: service

Description: Monitors the health of a cluster and attempts to identity potential outlier nodes. Helpful if there is a suspicion of a node under performing and impacting the overall cluster. This does not replace regular monitoring and alerting for a cluster but rather augments it. This has to be explicitly enabled on all the nodes for best results. See the [`health-stats`](https://aerospike.com/docs/database/reference/info#health-stats) and [`health-outliers`](https://aerospike.com/docs/database/reference/info#health-outliers) commands.

Introduced: 4.3.1.3

Removed: \-

Default Value: false

Detail:
**Example:** Set the enable-health-check to true dynamically:

```plaintext
asinfo -v "set-config:context=service;enable-health-check=true"
```

The statistics monitored are divided into `cluster stats` and `local stats`.  
Cluster statistics monitored consist of fabric connections opened, number of node arrivals, number of proxy requests and replica latency.  
Local statistic monitored consists of device read latency.

---

#### `enable-hist-info`

`dynamic` `cloud`

Context: service

Description: Enable histograms for info protocol transactions. See the [Histograms from Aerospike Logs](https://aerospike.com/docs/database/observe/latency) page for details.

Introduced: 3.9.0

Removed: \-

Default Value: false

Detail:
Here is the list of configuration enabled histograms:  

-   [`enable-benchmarks-batch-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-batch-sub)
-   [`enable-benchmarks-fabric`](https://aerospike.com/docs/database/reference/config#service__enable-benchmarks-fabric)
-   [`enable-benchmarks-ops-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-ops-sub)
-   [`enable-benchmarks-read`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-read)
-   [`enable-benchmarks-storage`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-storage)
-   [`enable-benchmarks-udf`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-udf)
-   [`enable-benchmarks-udf-sub`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-udf-sub)
-   [`enable-benchmarks-write`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-write)
-   [`enable-hist-info`](https://aerospike.com/docs/database/reference/config#service__enable-hist-info)
-   [`enable-hist-proxy`](https://aerospike.com/docs/database/reference/config#namespace__enable-hist-proxy)
-   [`sindex-histogram`](https://aerospike.com/docs/database/observe/latency)

**Example:** Set `enable-hist-info` to true:

```plaintext
asinfo -v 'set-config:context=service;enable-hist-info=true'
```

---

#### `enforce-best-practices`

`static` `cloud`

Context: service

Description: When set to `true`, Aerospike startup fails if any of the [best practices checks](https://aerospike.com/docs/database/learn/best-practices/#best-practices-checks) are violated. When set to `false`, Aerospike continues to start up and logs a warning for each failed best practice. It also sets the [`failed_best_practices`](https://aerospike.com/docs/database/reference/metrics#node_stats__failed_best_practices) metric to `true` and adds the name of the failed best practices to the output of the [`best-practices`](https://aerospike.com/docs/database/reference/info#best-practices) info command.

Introduced: 5.7.0

Removed: \-

Default Value: false

---

#### `feature-key-file`

`enterprise` `required` `static`

Context: service

Description: Specifies the [feature-key file](https://aerospike.com/docs/database/manage/planning/feature-key) needed to start up Enterprise Edition and Standard Edition server nodes.  

Value must follow one of these formats: Prefixes `file:`, `env:`, `env-b64:`, `vault:`, and `secrets:` are literal strings.

-   `file:/path/to/feature-key-file` - Reads from the filesystem (the `file:` prefix is optional). Starting with Database 5.5.0, up to 32 `feature-key-file` directives can be specified, with the server merging feature-keys from multiple sources. Path can also specify a directory, in which case all files within the directory must be feature-key files.
-   `env-b64:FEATUREKEY` - read from a named, base64-encoded environment variable (Database 5.4.0+).
-   `vault:feature-key` - the named secret will be read from [Vault](https://aerospike.com/docs/database/manage/security/vault) (Database 5.4.0+).
-   `secrets:AerospikeSecrets:FeatureKey` - fetched using [Aerospike Secret Agent](https://aerospike.com/docs/database/manage/security/secrets) (Database 6.4.0+).

Introduced: 4.0.0(optional) 4.6.0(required)

Removed: \-

Default Value: /etc/aerospike/features.conf

Detail:
The feature-key expiration date is only checked at startup. The Aerospike server continues to run after a feature-key expires, but fails to start or restart with an expired feature-key.:::

---

#### `group`

`static`

Context: service

Description: This configuration parameter is ignored when running with `--fgdaemon` or `--foreground` which is the way that the server is started on all current deployments using systemd or containers. See [Configure Aerospike to run as non-root](https://aerospike.com/docs/database/manage/database/non-root/).

Introduced: \-

Deprecated: 8.1.0

Removed: \-

Default Value: \-

---

#### `hist-track-back`

`static`

Context: service

Description: Total time span in seconds over which to cache data. This serves as a flag to enable/disable histograms. The reported track-back value can change at the generated namespace hist-track-back due to rounding based on the slice size. When the histogram is started, its number of rows is computed based on integer division of ‘back’ / ‘slice’. And while the number of rows and the slice size are stored with the histogram, the back size is not – it is recomputed from (# rows) \* (slice size) when being reported. So when the histogram is started, ‘back’ is effectively rounded down to the nearest multiple of ‘slice’, and corresponds to the actual time window tracked by the histogram.

Introduced: \-

Removed: 5.1.0

Default Value: 300

---

#### `hist-track-slice`

`static`

Context: service

Description: Period in seconds at which to cache histogram data.

Introduced: \-

Removed: 5.1.0

Default Value: 10

---

#### `hist-track-thresholds`

`static`

Context: service

Description: Comma-separated bucket (ms) values to track, must be powers of 2. For example : 1,4,16,64.

Introduced: \-

Removed: 5.1.0

Default Value: 1,8,64

Detail:
**Example:**

```asciidoc
hist-track-thresholds 1,2,4,8,16,32,64,128,256,512
```

---

#### `indent-allocations`

`static` `cloud`

Context: service

Description: Extra option for [`debug-allocations`](https://aerospike.com/docs/database/reference/config#service__debug-allocations) which enables detection of all double frees.

Introduced: 4.6.0

Removed: \-

Default Value: false

Detail:
When [`indent-allocations`](https://aerospike.com/docs/database/reference/config#service__indent-allocations) is enabled, the server will assert on detection of overwrites and all double frees. Also, each tracked allocation will incur a cost of 256 extra bytes.

---

#### `info-max-ms`

`dynamic` `cloud`

Context: service

Description: `info-max-ms` checks [info transactions](https://aerospike.com/docs/database/reference/info) for timeout after they are popped from the info transaction queue. The default value is 10000 milliseconds. The minimum is 500 ms, maximum 10000 ms.

Related to the [info\_timeout](https://aerospike.com/docs/database/reference/metrics#node_stats__info_timeout) metric, which tracks total timed-out info transactions.

Introduced: 6.3.0

Removed: \-

Default Value: 10000

---

#### `info-threads`

`dynamic` `cloud`

Context: service

Description: Number of threads to create to process info requests. This configuration is static in releases prior to 4.5.2. Maximum allowed value is 256 for Database 4.5.2 and later. Value range: 1-256.

Introduced: \-

Removed: \-

Default Value: 16

Detail:
**Example:** Set info-threads to 8 dynamically:

```plaintext
asinfo -v "set-config:context=service;info-threads=8"
```

---

#### `keep-caps-ssd-health`

`static` `cloud`

Context: service

Description: If `true`, enables non-root Aerospike users to keep permissions necessary to report (NVMe) device health. Currently, only ‘age’ is returned.

Introduced: \-

Removed: \-

Default Value: false

---

#### `log-local-time`

`static` `cloud`

Context: service

Description: By default, Aerospike server logs have a time stamp in GMT. Set this configuration to `true` to set logs to have local time stamp (also displays an offset to GMT).

Example: `Dec 12 2015 18:52:39 GMT-0800: INFO (as): (as.c::494) service ready: soon there will be cake!`

Introduced: 3.7.0.1

Removed: \-

Default Value: false

---

#### `log-millis`

`static` `cloud`

Context: service

Description: Set this to `true` in order to get millisecond timestamps in the log file.

Introduced: 3.1.03.0

Removed: \-

Default Value: false

---

#### `microsecond-histograms`

`dynamic` `cloud`

Context: service

Description: Set the granularity of histograms to microseconds instead of the default milliseconds. For the [auto enabled](https://aerospike.com/docs/database/observe/latency#auto-enabled-benchmarks) histograms, this configuration is static and nodes have to be restarted.

Introduced: 5.1.0

Removed: \-

Default Value: false

Detail:
**Example:** Set microsecond histograms to true:

```plaintext
asinfo -v "set-config:context=service;microsecond-histograms=true"
```

Histogram time unit cannot be changed while they are being written to the log file. For [auto-enabled-benchmarks](https://aerospike.com/docs/database/observe/latency#auto-enabled-benchmarks) which are always written to the log, a node restart is necessary to switch to microseconds. For configuration enabled benchmark histograms, it is necessary to turn those benchmark histograms off prior to dynamically changing the `microsecond-histograms` setting. Benchmark histograms are all the benchmarks that can be enabled through an `enable-benchmarks-xxx` configuration parameter. For example, [`enable-benchmarks-read`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-read) or [`enable-benchmarks-write`](https://aerospike.com/docs/database/reference/config#namespace__enable-benchmarks-write). See the full list on the [latency monitoring](https://aerospike.com/docs/database/observe/latency) page or on this configuration reference manual.

---

#### `migrate-fill-delay`

`enterprise` `dynamic` `cloud`

Context: service

Description: Number of seconds to delay before starting ‘fill’ migrations. For [Available mode](https://aerospike.com/docs/database/learn/architecture/clustering/consistency-modes#ap-mode) (AP), fill migrations are migrations that are going to a node that didn’t own a partition to be migrated. For [`strong-consistency`](https://aerospike.com/docs/database/reference/config#namespace__strong-consistency), these are migrations that are going to a non-roster-replica. These migrations aren’t necessary if the cluster state is transient (normal case) — when the cluster state is restored this migrated data would eventually be dropped. This setting doesn’t affect ‘lead migrations’ indicated by [`migrate_tx_partitions_lead_remaining`](https://aerospike.com/docs/database/reference/metrics#namespace__migrate_tx_partitions_lead_remaining). See the [Delaying “Fill” Migrations](https://aerospike.com/docs/database/manage/cluster/delay-migrations) page for further details.

Introduced: 4.3.1

Removed: \-

Default Value: 0

Detail:
**Example:** To enable a one hour fill delay across the cluster (to be changed in the configuration file as well since a restart will revert such dynamic change): `asadm -e "enable; asinfo -v 'set-config:context=service;migrate-fill-delay=3600'"`

For Database 5.2.0 and later, can be overridden for a namespace with the dynamic parameter [`ignore-migrate-fill-delay`](https://aerospike.com/docs/database/reference/config#namespace__ignore-migrate-fill-delay).  
  
For Database 4.5.0.2 and earlier, using time units (m, h, d) does not work when setting this configuration parameter dynamically.  
  
For [`strong-consistency`](https://aerospike.com/docs/database/reference/config#namespace__strong-consistency) enabled namespaces, when [`quiescing`](https://aerospike.com/docs/database/reference/info#quiesce), the `migrate-fill-delay` will only start ‘counting’ after the node is stopped.  
  
When increasing the `migrate-fill-delay` time, the extension applies from the initial point the migrations would have started.  
  
The `migrate-fill-delay` time is reset on any cluster change ([`cluster_size`](https://aerospike.com/docs/database/reference/metrics#node_stats__cluster_size) changing). For example, a full cluster shutdown with each node configured with a 1 hour delay (in the configuration file) will prevent ‘fill’ migrations from happening upon restarting of the cluster as long as there is at least 1 node re-joining the cluster every 1 hour (the [`cluster-stable`](https://aerospike.com/docs/database/reference/info#cluster-stable) command can be used to check that nodes are re-joining the cluster and the `migrate-fill-delay` can be dynamically updated if necessary).  
  
For use cases taking advantage of this setting, it is a good practice to set `migrate-fill-delay` in the configuration file to ensure that fill migrations do not kick in during a rolling restart which would reset any dynamically set parameter.

For [Available mode](https://aerospike.com/docs/database/learn/architecture/clustering/consistency-modes#ap-mode) (AP), if a stopped node either had its storage deleted or is configured to have an in-memory only namespace and wasn’t [`quiesced`](https://aerospike.com/docs/database/reference/info#quiesce) and fully migrated before being stopped, then the period of time where the cluster is unable to satisfy the durability requirement set by the [`replication-factor`](https://aerospike.com/docs/database/reference/config#namespace__replication-factor) configuration is extended by the `migrate-fill-delay`. Migrations will not start until the delay is up, or manually set to 0.

---

#### `migrate-max-num-incoming`

`dynamic` `cloud`

Context: service

Description: Maximum number of partitions a node can be receiving records from at any given time. The default value of 4 limits potential congestion on a given node, especially in situations where a node is added in a cluster. Can be increased cautiously to speed up migrations. See [manage migrations](https://aerospike.com/docs/database/manage/cluster/migrations#speeding-up-the-migration-rate) for further details. Maximum value is **256**.

Introduced: \-

Removed: \-

Default Value: 4

Detail:
**Example:** Set migrate-max-num-incoming to 8 dynamically:

```plaintext
asinfo -v "set-config:context=service;migrate-max-num-incoming=8"
```

Having higher allowed number of incoming partitions during migrations can, in some cases, adversely impact performance (especially when coupled with higher number of [`migrate-threads`](https://aerospike.com/docs/database/reference/config#service__migrate-threads)) and even cause unexpected bottleneck that would require restarting of nodes with a lower value. We recommend that you cautiously increase this parameter while monitoring network and disk IO for potential bottlenecks. Decreasing this value will only take effect after threads that are processing data have completed (full partition at a time).

---

#### `migrate-threads`

`dynamic` `cloud`

Context: service

Description: Number of threads per server allocated for data migration. Each thread will migrate one partition at a time. Increasing this parameter should be done with caution. See [manage migrations](https://aerospike.com/docs/database/manage/cluster/migrations#speeding-up-the-migration-rate) for further details. Value range: 0-100.

Introduced: \-

Removed: \-

Default Value: 1

Detail:
**Example:** Set migrate-threads to 2 dynamically:

```plaintext
asinfo -v "set-config:context=service;migrate-threads=2"
```

Decreasing this value will only take effect after threads that are processing data have completed (full partition at a time).

---

#### `min-cluster-size`

`dynamic` `cloud`

Context: service

Description: The minimum number of nodes required for a cluster to form. Necessary when configured with [`index-type flash`](https://aerospike.com/docs/database/reference/config#namespace__index-type) to avoid running out of resources in case of cluster splits.

Introduced: \-

Removed: \-

Default Value: 1

Detail:
**Example:** Set min-cluster-size dynamically to 6

```plaintext
asinfo -v "set-config:context=service;min-cluster-size=6"
```

When running in [`strong-consistency`](https://aerospike.com/docs/database/reference/config#namespace__strong-consistency) mode, if the desired `min-cluster-size` represents less than half the total number of nodes in the cluster, the `min-cluster-size` should not be configured. Indeed, minority sub-clusters make all partitions unavailable except the ones for which all the replicas are in the sub-cluster, so there is no new partition ownership, and no increase in index device space or DRAM required. This serves the same purpose as configuring `min-cluster-size`, but is better since there will be some availability in the sub-cluster. (If `min-cluster-size` is configured in such cases, eventually the nodes in the sub-cluster that can’t form will make everything unavailable.)  
  
Also, for [Available mode](https://aerospike.com/docs/database/learn/architecture/clustering/consistency-modes#ap-mode) (AP) namespaces the replication factor drops to 1 when a 1-node sub-cluster forms. So e.g. with replication factor 2, if `min-cluster-size` is not configured, a 1-node sub-cluster is no worse than a 2-node sub-cluster in terms of the resources required. Of course, large cluster, it is necessary to configure `min-cluster-size` significantly higher than 2 or 3.  
  
There are other less common situations where configuring `min-cluster-size` can help. For example, to prevent a fresh node not able to join a cluster to claim ownership of all partitions (for example issues resolving DNS in the cloud) or when running across multiple racks to prevent a single rack to form its own cluster if it separates from the other racks.

---

#### `node-id-interface`

`static`

Context: service

Description: Name of the interface from which to generate the ‘Node ID’. The ‘Node ID’ determines the succession list for partition assignments across nodes in a cluster.

Introduced: 3.10.0

Removed: \-

Default Value: \-

Detail:
The configuration file options [`node-id`](https://aerospike.com/docs/database/reference/config#service__node-id) and [`node-id-interface`](https://aerospike.com/docs/database/reference/config#service__node-id-interface) are mutually exclusive.

---

#### `node-id`

`static`

Context: service

Description: Allows specifying the `node-id` of the node as a 1 to 16 character (in hexadecimal), in order to make it friendlier or to influence the partition distribution which is based off the cluster’s node ids. By default, Aerospike derives the `node-id` from the configured fabric port and one of the server’s network interface mac address (or, if configured, the mac address of the [`node-id-interface`](https://aerospike.com/docs/database/reference/config#service__node-id-interface)).

Introduced: 3.16.0.1

Removed: \-

Default Value: N/A

Detail:
**Example:**

```asciidoc
service {

      <...>

      node-id a1

      <...>

  }
```

Node IDs can be changed one node at a time in a rolling fashion across a cluster.

Explicitly specifying the node ID is useful when leveraging a [shadow device](https://aerospike.com/docs/database/manage/namespace/storage/config/#setup-for-shadow-device) configuration that is network attached (for example an EBS volume on AWS) which would be re-attached against a different instance which by default would have a different node id than the original one and hence causing more migrations.

It is also useful for having human readable names to refer to different nodes in a cluster as well as configuring [`strong-consistency`](https://aerospike.com/docs/database/reference/config#namespace__strong-consistency) enabled namespaces [roster](https://aerospike.com/docs/database/reference/info#roster) information.

Changing the `node-id` in a [`strong-consistency`](https://aerospike.com/docs/database/reference/config#namespace__strong-consistency) enabled namespace would require re-setting the [roster](https://aerospike.com/docs/database/reference/info#roster) and should be done cautiously to avoid any availability and/or consistency impact.

A cluster will not accept 2 nodes with the same `node-id`. Having 2 nodes with the same `node-id` in a cluster would lead to erroneous and unexpected behavior. In particular, cluster size and data location would be incorrect and would result in poor performing and unusual data responses.

The configuration file options [`node-id`](https://aerospike.com/docs/database/reference/config#service__node-id) and [`node-id-interface`](https://aerospike.com/docs/database/reference/config#service__node-id-interface) are mutually exclusive.

---

#### `os-group-perms`

`static`

Context: service

Description: When set `true`, group read/write permissions are added to files created by the service.

Examples of affected files include storage files, system metadata (SMD) files, and log files.

Introduced: 5.6.0

Removed: \-

Default Value: false

---

#### `paxos-single-replica-limit`

`unanimous` `static`

Context: service

Description: If the cluster size is less than or equal to this value, only one copy of the data (no replicas) will be kept in the cluster. Only in [Available mode](https://aerospike.com/docs/database/learn/architecture/clustering/consistency-modes#ap-mode) (AP). Will be ignored for [`strong-consistency`](https://aerospike.com/docs/database/reference/config#namespace__strong-consistency) configured namespaces. Should typically be configured to a few nodes under the expected cluster size for clusters that would be used at near capacity (per the usual capacity sizing guidelines) but will depend on the total size of the cluster and how full the nodes are within the cluster.

Introduced: \-

Removed: 6.0.0

Default Value: 1

Detail:
As this configuration parameter is currently not dynamically configurable, See the [`migrate-fill-delay`](https://aerospike.com/docs/database/reference/config#service__migrate-fill-delay) for a way to prevent migrations from filling up remaining nodes when a cluster size is unexpectedly reduced.

This is useful when a cluster suddenly loses a node due to failure and the remaining nodes wouldn’t be able to accommodate as many replica copies as dictated by the configured [`replication-factor`](https://aerospike.com/docs/database/reference/config#namespace__replication-factor).

---

#### `pidfile`

`static`

Context: service

Description: This configuration parameter is ignored when running with `--fgdaemon` which is the way that the server is started on all current deployments using systemd. See [Configure Aerospike to run as non-root](https://aerospike.com/docs/database/manage/database/non-root/).

Introduced: \-

Deprecated: 8.1.0

Removed: \-

Default Value: /var/run/aerospike/asd.pid (in config)

Detail:
Not needed in a systemd environment. When using systemd a PID file is not created when specifying a pidfile in the service stanza of the aerospike.conf file. The logs will return a similar warning if pidfile is specified in the aerospike.conf file:

```plaintext
Oct 24 2018 21:20:55 GMT: WARNING (as): (as.c:337)

will not write PID file in new-style daemon mode
```

---

#### `proto-fd-idle-ms`

`dynamic`

Context: service

Description: This configuration parameter is obsolete. The Aerospike has been using keep-alive for client sockets since Database 4.8.0.

Introduced: \-

Deprecated: 8.1.0

Removed: \-

Default Value: 0

Detail:
Example: Set proto-fd-idle-ms to 70000 dynamically:

```plaintext
asinfo -v "set-config:context=service;proto-fd-idle-ms=70000"
```

Prior to Database 5.1.0, the default is 60000.

---

#### `proto-fd-max`

`dynamic` `cloud`

Context: service

Description: Maximum number of open file descriptors opened on behalf of client connections.

Can be increased for higher throughput use cases or for absorbing temporary spikes in traffic.  
Minimum: 1024. Maximum: 2097152.

At Aerospike server start, this value must not exceed the system’s file descriptor limit for the `asd` process. To avoid a startup problem, there are two alternatives:

-   Decrease the value of `proto-fd-max` in your Aerospike configuration file.
-   Increase the system’s file descriptor limit for the asd process.

Introduced: \-

Removed: \-

Default Value: 15000

Detail:
**Example:** Set proto-fd-max to 30000 dynamically. Prior to Database 4.9.0, for a dynamic change, this limit was enforced only if the new value was lower than the system setting.

```plaintext
asinfo -v "set-config:context=service;proto-fd-max=30000"
```

When hitting this limit, the client connections will be dropped and the following log message will be displayed:  
`WARNING (service): (service.c:419) (repeated:103799) refusing client connection - proto-fd-max 50000` This parameter has to be lower than the OS limit. For further details, see  
[https://support.aerospike.com/s/article/System-running-out-of-file-descriptors](https://support.aerospike.com/s/article/System-running-out-of-file-descriptors)

---

#### `proto-slow-netio-sleep-ms`

`dynamic`

Context: service

Description: This configuration specifies how long to sleep between repeated attempts when sending the response buffer for “slow” queries. Can be used as a throttling parameter during unexpected network congestion when response get re-queued.

Introduced: \-

Removed: 6.0.0

Default Value: 1ms

Detail:
**Example:** `asinfo -v "set-config:context=service;proto-slow-netio-sleep-ms=100"`

This configuration is not available to be set in the configuration file. Thus, on a server restart, this would need to be dynamically configured again.

---

#### `query-batch-size`

`dynamic`

Context: service

Description: Amount of disk I/O a query performs per I/O request. See the [Managing Queries](https://aerospike.com/docs/database/manage/cluster/queries) page for further details on tuning and configuring limits for secondary queries.

Introduced: \-

Removed: 6.0.0

Default Value: 100

Detail:
**Example:** Set query-batch-size to 75 dynamically:

```plaintext
asinfo -v "set-config:context=service;query-batch-size=75"
```

---

#### `query-buf-size`

`dynamic`

Context: service

Description: The unit of buffer size at which network IO is performed for secondary index queries. Used to avoid too many network calls.

This value can only be set dynamically. The value should be in bytes.

Decreasing this would mean more frequent network IO and improved response at the socket level.

Introduced: \-

Removed: 6.0.0

Default Value: 2097152

Detail:
**Example:** Set the query-buf-size to 500KiB dynamically:

```plaintext
asinfo -v "set-config:context=service;query-buf-size=512000"
```

---

#### `query-bufpool-size`

`dynamic`

Context: service

Description: This configuration specifies how many buffers to keep in a pool. This can be configured between the range of 1 to UINT32\_MAX. The unit of buffer size at which network IO is performed can be configured with [`query-buf-size`](https://aerospike.com/docs/database/reference/config#service__query-buf-size).

Introduced: \-

Removed: 5.7.0

Default Value: 256

Detail:
**Example:** `asinfo -v "set-config:context=service;query-bufpool-size=512"`

---

#### `query-in-transaction-thread`

`dynamic`

Context: service

Description: Run queries in transaction threads (Database 4.7.0 adn earlier) or service threads (Database 4.7.0 and later) instead of using query threads. Set it to ‘true’ when you expect queries to run for a short period of time or when the namespace is in-memory. Leave it set to ‘false’ if you expect longer running queries or if the namespace uses disk storage. See the [Managing Queries](https://aerospike.com/docs/database/manage/cluster/queries) page for further details on tuning and configuring limits for secondary queries.

Introduced: \-

Removed: 6.0.0

Default Value: false

Detail:
**Example:** Set query-in-transaction-thread to true dynamically:

```plaintext
asinfo -v "set-config:context=service;query-in-transaction-thread=true"
```

---

#### `query-long-q-max-size`

`dynamic`

Context: service

Description: Number of queries in the long running query queue. A long running query is one that returns more records than the `query-threshold`. See the [Managing Queries](https://aerospike.com/docs/database/manage/cluster/queries) page for further details on tuning and configuring limits for secondary queries.

Introduced: \-

Removed: 6.0.0

Default Value: 500

Detail:
**Example:** Set query-long-q-max-size to 600 dynamically:

```plaintext
asinfo -v "set-config:context=service;query-long-q-max-size=600"
```

---

#### `query-max-done`

`dynamic` `cloud`

Context: service

Description: Max number of finished query kept for monitoring. Value range: 0-1000.

Introduced: 6.0.0

Removed: \-

Default Value: 100

Detail:
**Example:** Set query-max-done to 500 dynamically:

```plaintext
asinfo -v "set-config:context=service;query-max-done=500"
```

---

#### `query-microbenchmark`

`dynamic`

Context: service

Description: Enable microbenchmarks of queries. This value can only be set dynamically.

Introduced: 3.3.10

Removed: 6.0.0

Default Value: false

Detail:
**Example:** Enable query-microbenchmark dynamically:

```plaintext
asinfo -v "set-config:context=service;query-microbenchmark=true"
```

---

#### `query-pre-reserve-partitions`

`dynamic`

Context: service

Description: This configuration can be used to pre-reserve all queryable partitions before processing a query. Enabling this to true might help reduce the potential inconsistency windows during ongoing migration for some use-cases, but can also have an adverse effect. Enterprise licensees can discuss specific use cases that could benefit from this parameter with Aerospike Support.

Introduced: \-

Removed: 5.7.0

Default Value: \-

Detail:
**Example:** `asinfo -v "set-config:context=service;query-pre-reserve-partitions=true"`

---

#### `query-priority-sleep-us`

`dynamic`

Context: service

Description: Time in microseconds that the server pauses after reading `query-priority` sequential query elements. See the [Managing Queries](https://aerospike.com/docs/database/manage/cluster/queries) page for further details on tuning and configuring limits for secondary queries.

Introduced: \-

Removed: 6.0.0

Default Value: 1

Detail:
**Example:** Set query-priority-sleep-us to 2 dynamically:

```plaintext
asinfo -v "set-config:context=service;query-priority-sleep-us=2"
```

---

#### `query-priority`

`dynamic`

Context: service

Description: Priority for query threads. Number of sequential query elements to read before yielding (for `query-sleep-us` micro seconds). A higher value is a higher priority. See the [Managing Queries](https://aerospike.com/docs/database/manage/cluster/queries) page for further details on tuning and configuring limits for secondary queries.

Introduced: \-

Removed: 6.0.0

Default Value: 10

Detail:
**Example:** Set query-priority to 20 dynamically:

```plaintext
asinfo -v "set-config:context=service;query-priority=20"
```

---

#### `query-rec-count-bound`

`dynamic`

Context: service

Description: This is the maximum number of records a query is allowed to return. A query returning beyond this limit is aborted. This can be configured between the range of 1 to UINT64\_MAX.

Introduced: \-

Removed: 6.0.0

Default Value: UINT64\_MAX

Detail:
**Example:** `asinfo -v "set-config:context=service;query-rec-count-bound=512"`

---

#### `query-req-in-query-thread`

`dynamic`

Context: service

Description: This configuration set to true will cause queries to always be processed in the main query thread and would not be queued to be processed by the [`query-worker-threads`](https://aerospike.com/docs/database/reference/config#service__query-worker-threads).

Introduced: \-

Removed: 6.0.0

Default Value: \-

Detail:
**Example:** `asinfo -v "set-config:context=service;query-req-in-query-thread=true"`

---

#### `query-req-max-inflight`

`dynamic`

Context: service

Description: Number of query I/O threads used per query at one time. See the [Managing Queries](https://aerospike.com/docs/database/manage/cluster/queries) page for further details on tuning and configuring limits for secondary queries.

Introduced: \-

Removed: 6.0.0

Default Value: 100

Detail:
**Example:** Set query-req-max-inflight to 150 dynamically:

```plaintext
asinfo -v "set-config:context=service;query-req-max-inflight=150"
```

---

#### `query-short-q-max-size`

`dynamic`

Context: service

Description: Number of queries in the short running query queue. A short running query is one that returns fewer records than the `query-threshold`. See the [Managing Queries](https://aerospike.com/docs/database/manage/cluster/queries) page for further details on tuning and configuring limits for secondary queries.

Introduced: \-

Removed: 6.0.0

Default Value: 500

Detail:
**Example:** Set query-short-q-max-size to 600 dynamically:

```plaintext
asinfo -v "set-config:context=service;query-short-q-max-size=600"
```

---

#### `query-threads-limit`

`dynamic` `cloud`

Context: service

Description: Maximum number of threads allowed for all queries. Can be dynamically increased or decreased. Value range: 1-1024.

Introduced: 6.0.0

Removed: \-

Default Value: 128

Detail:
**Example:** Set query-threads-limit to 64 dynamically:

```plaintext
asinfo -v "set-config:context=service;query-threads-limit=64"
```

---

#### `query-threads`

`dynamic`

Context: service

Description: Number of dedicated query threads on the node. Value range: 1-32. See the [Managing Queries](https://aerospike.com/docs/database/manage/cluster/queries) page for further details on tuning and configuring limits for secondary queries. Only even values are allowed from Database 5.7.0 and later. Odd values are rounded up to the next even number prior to Database 5.7.0.

Introduced: \-

Removed: 6.0.0

Default Value: 6

Detail:
**Example:** Set query-threads to 12 dynamically:

```plaintext
asinfo -v "set-config:context=service;query-threads=12"
```

---

#### `query-threshold`

`dynamic`

Context: service

Description: Dividing line between short running and long running queries. A query that returns fewer records than the `query threshold` is a short running query. All others are long running queries. See the [Managing Queries](https://aerospike.com/docs/database/manage/cluster/queries) page for further details on tuning and configuring limits for secondary queries.

Introduced: \-

Removed: 6.0.0

Default Value: 10

Detail:
**Example:** Set query-threshold to 20 dynamically:

```plaintext
asinfo -v "set-config:context=service;query-long-q-max-size=600"
```

---

#### `query-untracked-time-ms`

`dynamic`

Context: service

Description: Queries that run longer than this configured time are tracked by default. See the [Managing Queries](https://aerospike.com/docs/database/manage/cluster/queries) page for further details on tuning and configuring limits for secondary queries.

Introduced: \-

Removed: 6.0.0

Default Value: 1000

Detail:
**Example:** Set query-untracked-time-ms to 5 sec dynamically:

```plaintext
asinfo -v "set-config:context=service;query-untracked-time-ms=5000"
```

---

#### `query-worker-threads`

`dynamic`

Context: service

Description: Number of dedicated I/O threads on the node. See the [Managing Queries](https://aerospike.com/docs/database/manage/cluster/queries) page for further details on tuning and configuring limits for secondary queries.

Introduced: \-

Removed: 6.0.0

Default Value: 15

Detail:
**Example:** Set query-worker-threads to 20 dynamically:

```plaintext
asinfo -v "set-config:context=service;query-worker-threads=20"
```

---

#### `run-as-daemon`

`static`

Context: service

Description: If true, initial process forks into a new process (which runs in background) and exits.

Introduced: \-

Removed: \-

Default Value: true

Detail:
In 2.x the default is false.

---

#### `scan-threads-limit`

`dynamic`

Context: service

Description: Maximum number of threads allowed for all queries. Can be dynamically increased or decreased. Value range: 1-1024.

Introduced: 4.7.0

Removed: 6.0.0

Default Value: 128

Detail:
**Example:** Set scan-threads-limit to 64 dynamically:

```plaintext
asinfo -v "set-config:context=service;scan-threads-limit=64"
```

This parameter was renamed to [`query-threads-limit`](https://aerospike.com/docs/database/reference/config#service__query-threads-limit) in Database 6.0.0.

---

#### `secrets-address-port`

`enterprise` `static`

Context: service

Description: Specifies an IP address and port of the Secret Agent and TLS name specified in the TLS certificate. For a plain TCP connection between Aerospike Database and Secret Agent, only the IP address and port of Secret Agent need to be specified. For a TLS over TCP connection between the Aerospike database and Secret Agent, specify only the IP address, port of the Secret Agent, and TLS name mentioned in the TLS certificate, along with [`secrets-tls-context`](https://aerospike.com/docs/database/reference/config#service__secrets-tls-context). The TLS name should be either a common name or one of the Subject Alternate Names (SAN) in TLS certificate. User must specify either [`secrets-address-port`](https://aerospike.com/docs/database/reference/config#service__secrets-address-port) or [`secrets-uds-path`](https://aerospike.com/docs/database/reference/config#service__secrets-uds-path) but not both, to configure access to Secret Agent.

Introduced: 6.4.0

Removed: \-

Default Value: null

Detail:
**Example:**

Sample configuration file for a plain TCP connection between Aerospike server and Secret Agent:

```asciidoc
service {

  ...

  secrets-address-port 127.0.0.1 3005

  ...

}
```

Sample configuration file for a TLS over TCP connection between Aerospike server and Secret Agent:

```asciidoc
service {

  ...

  secrets-address-port 127.0.0.1 3005 secretagent #'secretagent' is a TLS name.

  secrets-tls-context secrets-tls

  ...

}

network {

  ...

  tls secrets-tls {

    ca-file /path/to/ca-file.pem

  }

  ...

}
```

---

#### `secrets-tls-context`

`enterprise` `static`

Context: service

Description: To establish a TLS connection over TCP between Aerospike server and Secret Agent, specify an IP address, port, and TLS name in [`secrets-address-port`](https://aerospike.com/docs/database/reference/config#service__secrets-address-port) along with a [`secrets-tls-context`](https://aerospike.com/docs/database/reference/config#service__secrets-tls-context). TLS name should be either a common name or one of the Subject Alternate Name (SAN) in TLS certificate.

Introduced: 6.4.0

Removed: \-

Default Value: null

Detail:
**Example:**

Sample configuration file for a TLS over TCP connection between Aerospike server and secret agent:

```asciidoc
service {

  ...

  secrets-address-port 127.0.0.1 3005 secretagent #'secretagent' is a TLS name.

  secrets-tls-context secrets-tls

  ...

}

network {

  ...

  tls secrets-tls {

    ca-file /path/to/ca-file.pem

  }

  ...

}
```

---

#### `secrets-uds-path`

`enterprise` `static`

Context: service

Description: This parameter specifies a Unix Domain Socket (UDS) path. To access a Secret Agent, you must set either [`secrets-uds-path`](https://aerospike.com/docs/database/reference/config#service__secrets-uds-path) or [`secrets-address-port`](https://aerospike.com/docs/database/reference/config#service__secrets-address-port) but not both. Use [`secrets-uds-path`](https://aerospike.com/docs/database/reference/config#service__secrets-uds-path) to communicate with a secret agent only if the Aerospike server and secret agent are running on the same host.

Introduced: 6.4.0

Removed: \-

Default Value: null

Detail:
**Example:** Sample configuration file to configure UDS:

```asciidoc
service {

  ...

  secrets-uds-path /path/to/uds.sock

  ...

}
```

---

#### `service-threads`

`dynamic` `cloud`

Context: service

Description: Number of threads receiving client requests and executing transactions. On multi-socketed systems, if Non-Uniform Memory Access (NUMA) pinning is enabled, each Aerospike instance only counts the CPU cores on the socket it is servicing.

-   Recommended and default value is five times the number of CPUs unless there are no SSD, memory, persistent memory (PMEM) namespaces with `commit-to-device` enabled, in which case the recommended and default value is the number of CPUs. The value range is 1-4096.

Introduced: \-

Removed: \-

Default Value: (5 × #cpu) or #cpu

Detail:
-   Prior to Database 5.1.0, all persistent memory (PMEM) namespaces also default to 5 per CPU.
-   Prior to 5.1, all persistent storage.
-   Prior to Database 4.7.0, this configuration item is static and defaults to the number of CPUs.

---

#### `sindex-builder-threads`

`dynamic` `cloud`

Context: service

Description: Number of threads for building secondary indexes. Can be set dynamically for secondary indexes created when a server is already running. When updating dynamically, the change goes into effect on a subsequent sindex build. The number of builder threads remains unchanged on a sindex build in progress. You should set this value in the configuration file for secondary indexes that are built or rebuilt during start up.

The maximum value is 32. See [Priority of secondary index creation](https://aerospike.com/docs/database/learn/architecture/data-storage/secondary-index/#priority-of-secondary-index-creation) for more information.

Introduced: 3.6.0

Removed: \-

Default Value: 4

Detail:
**Example:** `asinfo -v 'set-config:context=service;sindex-builder-threads=5'`

---

#### `sindex-gc-max-rate`

`dynamic`

Context: service

Description: The maximum processing rate (entries per second) for secondary index entries garbage collector. This refers to the number of records that have been indexed by a secondary index ([`entries`](https://aerospike.com/docs/database/reference/metrics#sindex__entries)).

Introduced: 3.1.04.0

Removed: 5.7.0

Default Value: 50000

Detail:
**Example:** `asinfo -v "set-config:context=service;sindex-gc-max-rate=10000"`

This is an upper bound. In general, if entries are garbage collected, the effective rate is lower.:::

---

#### `sindex-gc-period`

`dynamic` `cloud`

Context: service

Description: The interval (seconds) at which secondary index garbage collection thread runs.

Starting with Database 4.3.0, setting `sindex-gc-period` to a value of 0 will disable secondary index garbage collection.

Introduced: 3.1.04.0

Removed: \-

Default Value: 10

Detail:
**Example:** `asinfo -v "set-config:context=service;sindex-gc-period=100"`

If `sindex-gc-period` is dynamically set to zero while sindex garbage collection is in progress, the current cycle will complete, and then garbage collection will become dormant.

---

#### `stay-quiesced`

`enterprise` `static`

Context: service

Description: If set `true`, the node will start up [quiesced](https://aerospike.com/docs/database/reference/info#quiesce) and will remain quiesced. It will also ignore the [`quiesce-undo`](https://aerospike.com/docs/database/reference/info#quiesce-undo) command. For details on when to leverage this feature, see the [Quiescing a node](https://aerospike.com/docs/database/manage/cluster/quiesce-node) page.

Introduced: 5.2.0

Removed: \-

Default Value: false

---

#### `ticker-interval`

`dynamic` `cloud`

Context: service

Description: Global configuration for how often to print ‘ticker’ info to the log in seconds.

Introduced: \-

Removed: \-

Default Value: 10

Detail:
**Example:** Set ticker-interval to 20 dynamically:

```plaintext
asinfo -v "set-config:context=service;ticker-interval=20"
```

---

#### `tls-refresh-period`

`enterprise` `dynamic` `cloud`

Context: service

Description: Sets the time interval for refreshing the [`cert-file`](https://aerospike.com/docs/database/reference/config#network__cert-file), [`key-file`](https://aerospike.com/docs/database/reference/config#network__key-file) and [`cert-blacklist`](https://aerospike.com/docs/database/reference/config#network__cert-blacklist). Set to `0` to disable periodic refresh of TLS certificates.

Introduced: 7.1.0

Removed: \-

Default Value: 60

Detail:
**Example:**

Set `tls-refresh-period` to 100 seconds dynamically:

```plaintext
asinfo -v "set-config:context=service;tls-refresh-period=100s"
```

---

#### `transaction-max-ms`

`dynamic` `cloud`

Context: service

Description: How long to wait for success, in milliseconds before timing out a transaction on the server (typically, but not necessarily, during replica write or duplicate resolution). This would be overwritten by the client transaction timeout (if set). Transactions taking longer than this time (or the time specified in the client policy) will return a timeout and tick the [`client_write_timeout`](https://aerospike.com/docs/database/reference/metrics#namespace__client_write_timeout) metric.

Introduced: \-

Removed: \-

Default Value: 1000

Detail:
**Example:** Set transaction-max-ms to 2000 dynamically:

```plaintext
asinfo -v "set-config:context=service;transaction-max-ms=2000"
```

The `transaction-max-ms` (or, if specified, the client set timeout) gets checked in 4 different places:  

-   when processing of a transaction begins  
    
-   every 130ms (prior to Database 5.7.0, or 5ms for Database 6.0.0 and later) when waiting in the rw-hash (see [`rw_in_progress`](https://aerospike.com/docs/database/reference/metrics#node_stats__rw_in_progress))  
    
-   every 75ms (Database 5.7.0 or earlier or 5ms for Database 6.0.0 and later) when waiting in the proxy-hash (see [`proxy_in_progress`](https://aerospike.com/docs/database/reference/metrics#node_stats__proxy_in_progress))  
    
-   periodically during UDF execution  
      
    By default, a transaction will therefore not be retransmitted between server nodes (typically for write proles or duplicate resolution) if the client does not specify a transaction timeout (this is independent of the client retry policy). If a transaction timeout is specified by the client, or if the `transaction-max-ms` is increased, a transaction would be retried as many times as possible within this time frame. For example, if a client specifies a transaction timeout of 8 seconds, assuming there are network issues preventing a write to be processed on its prole side, the fabric transaction would be retried up to 3 times, with an interval starting at 1 second (default [`transaction-retry-ms`](https://aerospike.com/docs/database/reference/config#service__transaction-retry-ms)) and doubled for every subsequent retry.

---

#### `transaction-retry-ms`

`dynamic` `cloud`

Context: service

Description: How long to wait for success, in milliseconds, before retrying a transaction. [`migrate-retransmit-ms`](https://aerospike.com/docs/database/reference/config#namespace__migrate-retransmit-ms) is used for the migration related retransmits. The default of `1002` is meant to avoid retransmission by default based on the default [`transaction-max-ms`](https://aerospike.com/docs/database/reference/config#service__transaction-max-ms).

Introduced: \-

Removed: \-

Default Value: 1002

Detail:
**Example:** Set transaction-retry-ms to 500 dynamically:

```plaintext
asinfo -v "set-config:context=service;transaction-retry-ms=500"
```

---

#### `user`

`static`

Context: service

Description: This configuration parameter is ignored when running with `--fgdaemon` or `--foreground` which is the way that the server is started on all current deployments using systemd or containers. See [Configure Aerospike to run as non-root](https://aerospike.com/docs/database/manage/database/non-root/).

Introduced: \-

Deprecated: 8.1.0

Removed: \-

Default Value: \-

Detail:
Effective even before log file gets created.

---

#### `vault-ca`

`enterprise` `static`

Context: service

Description: [Vault integration](https://aerospike.com/docs/database/manage/security/vault) path to a TLS certificate on the node, used for authentication against the Vault service. The Vault integration is deprecated in favor of [Aerospike Secret Agent](https://aerospike.com/docs/database/manage/security/secrets/).

Introduced: 5.1.0

Deprecated: 8.1.0

Removed: \-

Default Value: \-

---

#### `vault-namespace`

`enterprise` `static`

Context: service

Description: Deprecated in Database 8.1.0. Use [Aerospike Secret Agent](https://aerospike.com/docs/database/tools/secret-agent/) instead. A string specifying the Vault namespace name. Only for use with Vault Enterprise. See the [Vault integration](https://aerospike.com/docs/database/manage/security/vault) documentation for further details.

Introduced: 6.3.0

Deprecated: 8.1.0

Removed: \-

Default Value: null

---

#### `vault-path`

`enterprise` `static`

Context: service

Description: Deprecated in Database 8.1.0. Use [Aerospike Secret Agent](https://aerospike.com/docs/database/tools/secret-agent/) instead. The path on the Vault system to the stored secret. See the [Vault integration](https://aerospike.com/docs/database/manage/security/vault) documentation for further details.

Introduced: 5.1.0

Deprecated: 8.1.0

Removed: \-

Default Value: \-

Detail:
Do not add the exact secret name as a suffix; this is supplied as the value of the Aerospike configuration parameter.

---

#### `vault-token-file`

`enterprise` `dynamic`

Context: service

Description: [Vault integration](https://aerospike.com/docs/database/manage/security/vault) path to a file that contains a token identifying the Aerospike cluster node to the Vault service. As of Database 6.3.0, you can dynamically update the `vault-token-file` value when a token file is already defined in the configuration file. Setting the `vault-token-file` to the same value dynamically forces the server to re-read it. The Vault integration is deprecated in favor of [Aerospike Secret Agent](https://aerospike.com/docs/database/manage/security/secrets/).

You can only update the value dynamically, not create it. In order to create a new `vault-token-file` configuration parameter, you must update your configuration file and restart the server.

If the configuration parameter is dynamically set to the same value, it forces a re-reading of the file and updates the token.

Prior to Database 6.3.0, `vault-token-file` is not dynamically settable. See the [Vault integration](https://aerospike.com/docs/database/manage/security/vault) documentation for further details.

Introduced: 5.1.0

Deprecated: 8.1.0

Removed: \-

Default Value: \-

Detail:
**Example:** Update the path to a Vault token:

```plaintext
asinfo -v "set-config:context=service;vault-token-file=/path/to/file"
```

Set a path to a Vault token in the configuration file:

```asciidoc
service {

  ...

  vault-token-file /path/to/file

  ...

}
```

---

#### `vault-url`

`enterprise` `static`

Context: service

Description: [Vault integration](https://aerospike.com/docs/database/manage/security/vault) URI defining the protocol, domain name, or IP address and port of the Vault service. The Vault integration is deprecated in favor of [Aerospike Secret Agent](https://aerospike.com/docs/database/manage/security/secrets/).

Introduced: 5.1.0

Deprecated: 8.1.0

Removed: \-

Default Value: \-

---

#### `work-directory`

`static`

Context: service

Description: Directory to be used by the Aerospike process to store all metadata and system files.

Introduced: \-

Removed: \-

Default Value: /opt/aerospike

Detail:
If this directory is user specified, the Aerospike process must have read/write permission on that directory.

---

## Xdr

#### `auth-mode`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc

Description: Specifies the authentication mode that XDR uses when security is enabled in the destination cluster. Allowed values are:

-   `none` - XDR does not attempt authentication.
    
    `none` is the only mode allowed when [`connector`](https://aerospike.com/docs/database/reference/config#xdr__connector) is set to `true` on the destination cluster, otherwise the following error is logged: `DC <DC_NAME> can't set 'auth-mode' if 'connector' is 'true'`
    
-   `internal` - The destination cluster uses a hashed password to validate user credentials.
    
-   `external` - The destination cluster validates user credentials externally, for example using LDAP. [TLS](https://aerospike.com/docs/database/learn/security/tls) is required when using this mode, as the user password is sent as clear text.
    
-   `external-insecure` - The destination cluster validates user credentials externally, for example using LDAP. TLS is not required for this mode. This mode is not recommended for production systems because the user password is sent as clear text.
    
-   `pki` - Available in Database 5.7.0 and later, this mode uses the common-name (CN) in the TLS certificate as the user name. You must configure [`tls-name`](https://aerospike.com/docs/database/reference/config#xdr__tls-name) when using this mode, but you do not need to specify [`auth-user`](https://aerospike.com/docs/database/reference/config#xdr__auth-user) or [`auth-password-file`](https://aerospike.com/docs/database/reference/config#xdr__auth-password-file).

Introduced: 4.7.0

Removed: \-

Default Value: none (as of 5.7)

Detail:
-   In Database 5.6.0 and earlier, the default value is `internal`. If `auth-user` is set, authentication is attempted automatically. Starting in Database 5.7.0, this parameter should be explicitly set to an appropriate value other than `none` to attempt authentication.
-   Set this parameter _before_ connecting to the remote datacenter. If you attempt to set this parameter dynamically when the remote datacenter is connected, the `asinfo` command generates an error.
-   If you have already connected to the remote datacenter and you are having trouble setting this parameter, remove the namespace to disconnect, set the parameter, then add the namespace again. To learn more about the `asinfo` commands you need to use, see [`namespace`](https://aerospike.com/docs/database/reference/config#xdr__namespace) in the XDR `dc` subcontext.

---

#### `auth-password-file`

`enterprise` `dynamic`

Context: xdr

Subcontext: dc

Description: Specifies the password of the XDR [`auth-user`](https://aerospike.com/docs/database/reference/config#xdr__auth-user). This user must have read/write permissions on a destination node that has `security-enabled true`.

Value must follow one of these formats. Prefixes `file:`, `env:`, `env-b64:`, `vault:`, and `secrets:` are literal strings.

-   `file:/path_to/xaupwd` - Read from the filesystem (the `file:` prefix is optional).
-   `env:XAUPWD` - Read from the named environment variable (Database 5.3.0+).
-   `vault:auth-password` - the named secret will be read from [Vault](https://aerospike.com/docs/database/manage/security/vault) (Database 5.1.0+).
-   `secrets:AerospikeSecrets:AuthPassword` - fetched using [Aerospike Secret Agent](https://aerospike.com/docs/database/manage/security/secrets) (Database 6.4.0+).

Introduced: 5.0.0

Removed: \-

Default Value: \-

Detail:
Content of the file is the password of the user:

```plaintext
passwordOnDestination
```

**Example:**

```asciidoc
dc dataCenter1 {

  node-address-port someIpAddress1 somePort1

  ...

  auth-user someUser

  auth-password-file /private/security-credentials_DC1.txt

  ...

  }

 }
```

Set `auth-password-file` dynamically:

```plaintext
asinfo -v "set-config:context=xdr;dc=DC1;auth-password-file=/private/security-credentials_DC1.txt"
```

This is not allowed for ‘connector’ datacenters.

Set this parameter _before_ connecting to the remote datacenter. It can be set dynamically only when the remote datacenter is not connected; otherwise, the `asinfo` command will return an error.

If you have already connected to the remote datacenter and are encountering difficulties, remove the namespace to disconnect, then set the parameter, and then re-add the namespace. For details on the necessary `asinfo` commands, see the configuration parameter for [`namespace`](https://aerospike.com/docs/database/reference/config#xdr__namespace) in the XDR `dc` subcontext.

In Aerospike Database 5.1.0.3, setting `auth-user` _without previously setting `auth-password-file`_ will cause a crash.

In Database 5.0.0.10 and earlier, and Database 5.1.0.3, setting`auth-password-file` while connected to the datacenter may cause a crash.

---

#### `auth-user`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc

Description: For XDR, specifies the name of a user who has read/write permissions on a destination node that has `security-enabled true`.

For background, see [Securing XDR with access control, LDAP, and TLS](https://aerospike.com/docs/database/manage/xdr/security).

Introduced: 5.0.0

Removed: \-

Default Value: \-

Detail:
**Example:**

```asciidoc
xdr {

   dc dataCenter1 {

     node-address-port someIpAddress1 somePort1

     ...

     auth-user someUser

     auth-password-file /private/security-credentials_DC1.txt

     ...

     }

    }
```

Set `auth-user` dynamically:

```plaintext
asinfo -v "set-config:context=xdr;dc=DC1;auth-user=someUser"
```

This is not allowed for ‘connector’ datacenters.

Set this parameter _before_ connecting to the remote datacenter. It can be set dynamically only when the remote datacenter is not connected; otherwise, the `asinfo` command will return an error.

If you have already connected to the remote datacenter and are encountering difficulties, remove the namespace to disconnect, then set the parameter, and then re-add the namespace. For details on the necessary `asinfo` commands, see the configuration parameter for [`namespace`](https://aerospike.com/docs/database/reference/config#xdr__namespace) in the XDR `dc` subcontext.

In Aerospike Database 5.1.0.3, setting `auth-user` _without previously setting [`auth-password-file`](https://aerospike.com/docs/database/reference/config#xdr__auth-password-file)_ will cause a crash.

---

#### `bin-policy`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc/namespace

Description: Determines which bins are shipped to the target datacenter. Allowable values:

-   `all` (default)
-   `no-bins`
-   `only-changed`
-   `only-specified` (removed as of Database 5.3.0)
-   `changed-and-specified`
-   `changed-or-specified`  
      
    Some restrictions apply based on the configured [`write-policy`](https://aerospike.com/docs/database/reference/config#xdr__write-policy). See the [bin policy documentation page](https://aerospike.com/docs/database/manage/xdr/bin-policy).

Introduced: 5.2.0

Removed: \-

Default Value: all

Detail:
**Example:**

```asciidoc
xdr {

  dc DC1 {

    node-address-port 10.1.0.1 3000

    namespace nameSpaceName {

      bin-policy only-changed

      ...

    }

  }

}
```

Set `bin-policy` dynamically:

```asciidoc
asinfo -v "set-config:context=xdr;dc=DC1;namespace=nameSpaceName;bin-policy=only-changed"
```

---

#### `compression-level`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc/namespace

Description: **Note**: This is XDR `compression-level` for `dc` `namespace`,not [`compression-level` for `storage-engine`](https://aerospike.com/docs/database/reference/config#namespace__compression-level).

Compression level of data-in-transit to remote destinations.

Allowable range: 1 to 9. A higher value, for example 9, means more efficient but slower compression. A lower value, for example 1, means less efficient but faster compression.

Requires [`enable-compression`](https://aerospike.com/docs/database/reference/config#xdr__enable-compression) `true`; otherwise, no compression is applied.

See also the metric [`compression_ratio`](https://aerospike.com/docs/database/reference/metrics#xdr__compression_ratio).

Introduced: 5.1.0

Removed: \-

Default Value: 1

Detail:
**Example:** Set `compression-level` to 6 (the compression level of XDR 4.X) in the configuration file.

```asciidoc
xdr {

    dc dataCenter1 {

        node-address-port someIpAddress1 somePort1

        namespace someNameSpaceName {

        ...

        enable-compression true

        compression-level 6

        ...

        }

    }

}
```

Set `compression-level` dynamically to 6 (the compression level of XDR 4.X):

```asciidoc
asinfo -v 'set-config:context=xdr;dc=DataCenter1;namespace=someNameSpace;enable-compression=true;'

 asinfo -v 'set-config:context=xdr;dc=DataCenter1;namespace=someNameSpace;compression-level=6
```

---

#### `compression-threshold`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc/namespace

Description: Record size threshold, in bytes. When at or greater than this threshold, a record will be compressed for transit to remote destinations.

Only applicable when [`enable-compression`](https://aerospike.com/docs/database/reference/config#xdr__enable-compression) is `true`.

Allowable range is 128 to UINT32\_MAX.

Introduced: 6.0.0

Removed: \-

Default Value: 128

Detail:
**Example:** Set `compression-threshold` to 512.

```asciidoc
xdr {

  dc DC1 {

    node-address-port 10.1.0.1 3000

    namespace nameSpaceName {

       enable-compression true

       compression-threshold 512

    }

  }

}
```

Set `compression-threshold` dynamically to 512:

```asciidoc
asinfo -v 'set-config:context=xdr;dc=DataCenter1;namespace=someNameSpace;compression-threshold=512'
```

---

#### `connector`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc

Description: Allowed values are:

-   `true` - Indicates that the destination is a server running an Aerospike connector capable of receiving change notification messages.
-   `false` - Indicates that the destination is also an Aerospike cluster.

Introduced: 5.0.0

Removed: \-

Default Value: false

Detail:
You should set this parameter _before_ connecting to the remote datacenter. It can be set dynamically _only_ when the remote datacenter is not connected; otherwise, the `asinfo` command will error.  
  
If you have already connected to the remote datacenter and are encountering difficulties, you need to remove the namespace to disconnect, then set the parameter, and then re-add the namespace. For details on the necessary `asinfo` commands, see the configuration parameter for [`namespace`](https://aerospike.com/docs/database/reference/config#namespace) in the XDR `dc` subcontext.

---

#### `datacenter`

`enterprise` `static`

Context: xdr

Description: Specifies the name of a remote datacenter for XDR. Name of the remote datacenter is user-defined. In Aerospike Database 5.0.0 and later, this parameter is replaced by [`dc`](https://aerospike.com/docs/database/reference/config#xdr__dc).

Introduced: \-

Removed: 5.0.0

Default Value: none

Detail:
**Example:** Below is an example of the `datacenter` parameter:

```asciidoc
xdr {

     enable-xdr true

     datacenter DC1 {

             dc-node-address-port xx.xx.xx.xx 3000

             dc-node-address-port yy.yy.yy.yy 3000

             dc-node-address-port zz.zz.zz.zz 3000

     }

}
```

---

#### `dc-connections-idle-ms`

`enterprise` `dynamic`

Context: xdr

Subcontext: datacenter

Description: This idle time before a connection is closed on the XDR client. This should always be set to a few seconds lower than the corresponding destination(s) [proto-fd-idle-ms](https://aerospike.com/docs/database/reference/config#service__proto-fd-idle-ms) to avoid race conditions where the destination closes a connection right when the XDR client is sending a new record on it.  
XDR is very sensitive to connection errors and will throttle when encountering such errors, potentially resulting in lag and outstanding digest increases.

Introduced: 3.14.1.1

Removed: 5.0.0

Default Value: 55000

Detail:
**Example:** Dynamically increasing the connections idle time to 85 seconds:

```asciidoc
asinfo -v "set-config:context=xdr;dc=DC1;dc-connections-idle-ms=85000"
```

---

#### `dc-connections`

`enterprise` `static`

Context: xdr

Subcontext: datacenter

Description: The number of connections to open per destination node. This typically should not be changed, but for specific low throughput workloads, decreasing the number of connections avoids running into idle connections being terminated by the destination node which is based on the [proto-fd-idle-ms](https://aerospike.com/docs/database/reference/config#service__proto-fd-idle-ms) setting.

XDR is very sensitive to connection errors and will throttle when encountering such errors, potentially resulting in lag and outstanding digest increases.

Introduced: 3.14.1.1

Removed: 5.0.0

Default Value: 64

Detail:
**Example:** Dynamically reducing the number of connections for DC1 to 8:

```asciidoc
asinfo -v "set-config:context=xdr;dc=DC1;dc-connections=8"
```

In Database 4.5.3.2 to 4.5.3.14, 4.6.0.2 to 4.6.0.12, 4.7.0.2 to 4.7.0.10, and 4.8.0.1 to 4.8.0.5 increasing the dc-connections dynamically causes a crash. This configuration parameter is now static.

---

#### `dc-int-ext-ipmap`

`enterprise` `dynamic`

Context: xdr

Subcontext: datacenter

Description: Use [dc-use-alternate-services](https://aerospike.com/docs/database/reference/config#xdr__dc-use-alternate-services) and [`alternate-access-address`](https://aerospike.com/docs/database/reference/config#network__alternate-access-address) at the destination nodes instead of `dc-int-ext-ipmap`. Mapping of the internal IPs of nodes of the remote cluster to their corresponding external IPs.

Introduced: 3.3.0

Removed: 5.0.0

Default Value: \-

Detail:
**Example:** Mapping of Internal to External IP

```asciidoc
dc-int-ext-ipmap 192.168.1.1 204.153.101.101

dc-int-ext-ipmap 192.168.1.2 204.153.101.102

...
```

Dynamic changes

```asciidoc
asinfo -p <XDRPORT> -v 'config-set:context=xdr;dc=<DATACENTER>;dc-int-ext-ipmap=<INTERNAL_IP>/<EXTERNAL_IP>;action=add'

 asinfo -p <XDRPORT> -v 'config-set:context=xdr;dc=<DATACENTER>;dc-int-ext-ipmap=<INTERNAL_IP>/<EXTERNAL_IP>;action=remove'
```

To be used when the remote cluster’s nodes publish private IP addresses through `access-address`.

Dynamically changeable. If you make dynamic changes to this configuration, be sure to include the XDR port number. The default XDR port number is 3004.

---

#### `dc-node-address-port`

`enterprise` `dynamic`

Context: xdr

Subcontext: datacenter

Description: Replaced in Aerospike 5.0.0 with [`node-address-port`](https://aerospike.com/docs/database/reference/config#xdr__node-address-port).  
  
The address & port of a node in the remote datacenter. Can be set dynamically.

Introduced: \-

Removed: 5.0.0

Default Value: \-

Detail:
**Example:** Dynamically adding and removing of a node for DC1:

```asciidoc
asinfo -v "set-config:context=xdr;dc=DC1;dc-node-address-port=192.168.55.210:3000;action=add"

asinfo -v "set-config:context=xdr;dc=DC1;dc-node-address-port=192.168.55.210:3000;action=remove"
```

Ipv6 example

```asciidoc
asinfo -v "set-config:context=xdr;dc=DC1;dc-node-address-port=[fe80::20c:29ff:fea9:df10]:3000;action=add"

asinfo -v "set-config:context=xdr;dc=DC1;dc-node-address-port=[fe80::20c:29ff:fea9:df10]:3000;action=remove"
```

Multiple nodes can be specified. Used as a seed list. Recommended to prefer static configuration rather then dynamic to avoid issues upon restart.

---

#### `dc-security-config-file`

`enterprise` `dynamic`

Context: xdr

Subcontext: datacenter

Description: Replaced in Aerospike 5.0.0 with [`auth-password-file`](https://aerospike.com/docs/database/reference/config#xdr__auth-password-file) and [`auth-user`](https://aerospike.com/docs/database/reference/config#xdr__auth-user).

Specifies the credentials file to be used by XDR to ship to the DC. User must have write or read-write permissions.

Introduced: 3.8.1

Removed: 5.0.0

Default Value: \-

Detail:
File syntax:

```plaintext
credentials

{

  username xdr_user

  password xdr_pass

}
```

To dynamically specify this use the following command:

```plaintext
asinfo -v "set-config:context=xdr;dc=DC1;dc-security-config-file=/private/aerospike/security_credentials_DC1.txt"
```

This command would trigger a reconnection to the cluster to avoid having a mix of connections using different credentials.

To dynamically unset the security config file:

```plaintext
asinfo -v "set-config:context=xdr;dc=DC1;dc-security-config-file=none"

``` See [XDR Advanced Configuration](/database/manage/xdr/static-xdr/#example-configuration-parameters-for-xdr-topologies) for further details.

**Example:**

XDR stanza

```asciidoc

...

xdr {

  enable-xdr true

  xdr-digestlog-path /opt/aerospike/xdr/digestlog 100G

  datacenter DC1 {

   dc-node-address-port xx.xx.xx.xx 3000

   dc-node-address-port yy.yy.yy.yy 3000

   dc-node-address-port zz.zz.zz.zz 3000

   dc-use-alternate-services true

   dc-security-config-file /private/aerospike/security_credentials_DC1.txt

  }

  ...

  $ more /private/aerospike/security-credentials_DC1.txt

  credentials

  {

     username xdr_user

     password xdr_pass

  }
```

---

#### `dc-ship-bins`

`enterprise` `dynamic`

Context: xdr

Subcontext: datacenter

Description: If `false`, bin shipping optimization is disabled at DC level. Refer [`xdr-ship-bins`](https://aerospike.com/docs/database/reference/config#xdr__xdr-ship-bins) to know about bin shipping optimization.

Introduced: 4.5.2

Removed: 5.0.0

Default Value: true

Detail:
To dynamically specify this use the following command:

```plaintext
asinfo -v "set-config:context=xdr;dc=DC1;dc-ship-bins=false"
```

This configuration will override `xdr-ship-bins` only from `true` to `false` at DC level. In other words, setting `xdr-ship-bins` to `false` and setting `dc-ship-bins` to `true` will not enable bin shipping optimization for a DC.

---

#### `dc-type`

`enterprise` `dynamic`

Context: xdr

Subcontext: datacenter

Description: Allowed values are:

-   `aerospike` - Indicates that the destination is also an aerospike cluster.
-   `http` - Indicates that the destination is a webserver capable of receiving change notification messages.  
    Though this config option is dynamic, only the type of skeleton DCs can be changed to `http` (from the default `aerospike`). Once the type is set as `http`, its type cannot be changed to `aerospike`. If the type is changed dynamically by mistake, the node should be restarted with the correct configuration. Changes to this configuration should be planned accordingly. See [Configuring change notification](https://aerospike.com/docs/connectors/streaming/common/change-notification) for further details.

Introduced: 4.4.0

Removed: 5.0.0

Default Value: aerospike

---

#### `dc-use-alternate-services`

`enterprise` `dynamic`

Context: xdr

Subcontext: datacenter

Description: Replaced in Aerospike 5.0.0 with [`use-alternate-access-address`](https://aerospike.com/docs/database/reference/config#xdr__use-alternate-access-address).  
  
If alternate-access-address is set on the destination nodes, specify dc-use-alternate-services true at the source nodes in order to use the services-alternate IP addresses to connect to the destination nodes (instead of services). To be used when the remote cluster’s nodes publish IP addresses through [`access-address`](https://aerospike.com/docs/database/reference/config#network__access-address) which are not accessible over WAN and alternate IP addresses accessible over WAN through [`alternate-access-address`](https://aerospike.com/docs/database/reference/config#network__alternate-access-address).

Introduced: 3.8.1

Removed: 5.0.0

Default Value: \-

Detail:
**Example:** Set dc-use-alternate-services to true post 3.14.1.1:

```plaintext
asinfo -v "set-config:context=xdr;dc=<dc-name>;dc-use-alternate-services=true"
```

---

-   Can only be set dynamically if the DC is in the CLUSTER\_INACTIVE state (without seeds or unused by namespaces). Will error otherwise.:::

---

#### `dc`

`enterprise` `dynamic`

Context: xdr

Description: Specifies the name of a remote datacenter for XDR. Name of the remote datacenter is user-defined. The maximum number of `dc` definitions is 64. The maximum length of a single definition is 31 bytes. Stay within the ASCII character set to avoid using a double-byte character and exceeding the size limit.

-   Prior to Aerospike Database 5.7.0, at least one DC needs to be configured statically to enable XDR.
-   Prior to Database 5.0.0, this parameter was named `datacenter`.

Introduced: 5.0.0

Removed: \-

Default Value: none

Detail:
Example

```asciidoc
xdr {

  dc DC1 {

     node-address-port xx.xx.xx.xx 3000

     node-address-port yy.yy.yy.yy 3000

     node-address-port zz.zz.zz.zz 3000

     namespace someNameSpaceName {

        ...

     }

  }

}
```

-   Set the `dc` parameter dynamically:
    
    ```plaintext
    asinfo -h localhost -v "set-config:context=xdr;dc=aerospike_b;action=create"
    ```
    
-   Set the XDR `namespace` parameter dynamically:
    
    ```plaintext
    asinfo -h localhost -v "set-config:context=xdr;dc=aerospike_b;namespace=test;action=add"
    ```
    

**When adding a namespace that already exists, `asinfo` returns an error and logs a warning:**

```plaintext
asadm -e 'asinfo -v "set-config:context=namespace;id=NAMESPACE;xdr-remote-datacenter=DCNAME;action=add"

ERROR:4:invalid state or set-config parameter
```

The logged warning is: `{<ns-name>} DC %s namespace already added`

**When removing a namespace that doesn’t exist, `asinfo` returns an error and logs a warning:**

```plaintext
asadm -e 'asinfo -v "set-config:context=namespace;id=NAMESPACE;xdr-remote-datacenter=DCNAME;action=remove"

ERROR:4:invalid state or set-config parameter
```

The logged warning is: `{<ns-name>} DC %s namespace already removed`

Prior to Aerospike 8.1.0, neither case returned an error.

---

#### `delay-ms`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc/namespace

Description: Value in milliseconds as an artificial delay on shipment of all records, including hotkeys and records that are not hot. Minimum value is 0 and maximum value is 5000.

-   Must be less than or equal to the value of [`hot-key-ms`](https://aerospike.com/docs/database/reference/config#xdr__hot-key-ms).
-   Must be 0 if [`ship-versions-policy`](https://aerospike.com/docs/database/reference/config#xdr__ship-versions-policy) is `all`.
-   Cannot exceed the time window specified by [`ship-versions-interval`](https://aerospike.com/docs/database/reference/config#xdr__ship-versions-interval).

Introduced: 5.0.0

Removed: \-

Default Value: 0

Detail:
**Example:**

Decreasing `delay-ms` increases the frequency of shipping of all records.

---

#### `enable-change-notification`

`enterprise` `static`

Context: xdr

Description: In Aerospike 5.0.0, this parameter is no longer needed.  
  
This configuration initializes the change notification framework in the server (XDR). Unless this configuration is set to true, HTTP destination types cannot be configured. See [change notification](https://aerospike.com/docs/connectors/streaming/common/change-notification) for further details.  
Requires a feature the `asdb-change-notification` feature-key be enabled in the [`feature-key-file`](https://aerospike.com/docs/database/reference/config#service__feature-key-file).

Introduced: 4.4.0

Removed: 5.0.0

Default Value: false

---

#### `enable-compression`

`enterprise` `dynamic`

Context: xdr

Subcontext: dc/namespace

Description: For Aerospike 5.0.0 and later, by default, compression is disabled.

For Aerospike 5.0.0 through 5.7, the compression threshold is internally set at record sizes of 128 bytes or more. For Aerospike 6.0.0 and later, the compression threshold is specified by the [`compression-threshold`](https://aerospike.com/docs/database/reference/config#xdr__compression-threshold) parameter.

If set to `true`, the lowest level of compression is applied by default (1). To set a compression level other than the default, see related parameter `compression-level` for XDR `dc` `namespace`.  
  
The compression algorithm is [zlib](https://www.zlib.net/).

Introduced: 5.0.0

Removed: \-

Default Value: false

Detail:
**Example:**

```asciidoc
xdr {

  dc DC1 {

    node-address-port 10.1.0.1 3000

    namespace nameSpaceName {

       enable-compression true

    }

  }

}
```

Set `enable-compression` dynamically:

```plaintext
asinfo -v "set-config:context=xdr;dc=DC1;namespace=namespaceName;enable-compression=true"
```

---

#### `enable-xdr`

`enterprise` `dynamic`

Context: xdr

Description: In Aerospike 5.0.0, this parameter is no longer needed.  
  
Enable record entries to be written to the XDR digest log for the node globally, letting the `enable-xdr` namespace level setting take effect at the namespace level. This controls whether digest log entries are being written to the digest log. This therefore practically controls whether records are being shipped through XDR globally, assuming DCs are configured and available, [xdr-shipping-enabled](https://aerospike.com/docs/database/reference/config#xdr__xdr-shipping-enabled) is kept at its default value (true) and the `enable-xdr` configuration is set to true at the respective namespaces.  
Configured DCs that are linked to namespaces will be connected to independently of the value of this setting. To prevent the connections from being made, you will need to either a) [remove all seed nodes](https://aerospike.com/docs/database/reference/config#xdr__dc-node-address-port) from the datacenter definition, or b) [remove the datacenter](https://aerospike.com/docs/database/reference/config#namespace__xdr-remote-datacenter) from all namespace definitions, or do so dynamically to break existing connections.

Introduced: \-

Removed: 5.0.0

Default Value: false

Detail:
**Example:** Set `enable-xdr` to true dynamically:

```plaintext
asinfo -v "set-config:context=xdr;enable-xdr=true"
```

---

#### `forward-xdr-writes`

`enterprise` `dynamic`

Context: xdr

Description: Replaced in Aerospike 5.0.0 by [`forward`](https://aerospike.com/docs/database/reference/config#xdr__forward).  
  
By default XDR writes that originated from another XDR are not forwarded to the specified destination datacenters. Setting this parameter to true will forward writes that originated from another XDR to the specified destination datacenters.

Introduced: \-

Removed: 5.0.0

Default Value: false

Detail:
**Example:** Set forward-xdr-writes to true dynamically:

```plaintext
asinfo -v "set-config:context=xdr;forward-xdr-writes=true"
```

To dynamically change you must target ASD’s service port, not XDR.

If setting to ‘true’ be aware of your topology and ensure you aren’t creating a forwarding loop.

---

#### `forward`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc/namespace

Description: By default XDR writes that originated from another XDR are not forwarded to the specified destination datacenters. Setting this parameter to true sends writes that originated from another XDR to the specified destination datacenters. See simple topology example in [Linear chain](https://aerospike.com/docs/database/manage/xdr/static-xdr#linear-chain).

Introduced: 5.0.0

Removed: \-

Default Value: false

Detail:
**Example:**

```asciidoc
xdr {

  dc DC1 {

    node-address-port 10.1.0.1 3000

    namespace nameSpaceName {

       forward true

    }

  }

}
```

Set `forward` dynamically:

```plaintext
asinfo -v "set-config:context=xdr;dc=DC1;namespace=namespaceName;forward=true"
```

If you set to ‘true’, be aware of your topology and ensure you aren’t creating a forwarding loop.

This cannot be used if bin convergence is turned on.

---

#### `hot-key-ms`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc/namespace

Description: Time (in milliseconds) to wait in between shipping hotkeys, which are records that change frequently. See also [`delay-ms`](https://aerospike.com/docs/database/reference/config#xdr__delay-ms).  
  
Minimum: 0.  
Maximum: 5000.  
  
Replaces `xdr-hotkey-time-ms`.

Introduced: 5.0.0

Removed: \-

Default Value: 100

Detail:
**Example:**

```asciidoc
xdr {

  dc DC1 {

    node-address-port 10.1.0.1 3000

    namespace nameSpaceName {

      hot-key-ms 1000

    }

  }

}
```

Set `hot-key-ms` dynamically:

```plaintext
asinfo -v "set-config:context=xdr;dc=DC1;namespace=namespaceName;hot-key-ms=1000"
```

Decreasing `hot-key-ms` increases the frequency of shipping hotkeys to destination clusters.

---

#### `http-url`

`enterprise` `dynamic`

Context: xdr

Subcontext: datacenter

Description: This specifies the URL to which the [change notification](https://aerospike.com/docs/connectors/streaming/common/change-notification) will publish the events. A webserver should be listening here to acknowledge the notification and process them. Multiple lines of this configuration can be used to specify multiple URLs. When multiple URLs are specified, XDR will load balance between them.

If the URL starts with `https`, secure communication will be used. Else, if it starts with `http`, plain text communication will be used. If a directory/file other than the system default should be used for certificate validation during https communication, it can be done with `tls-name` config option of the datacenter. The corresponding tls spec’s ca-cert/ca-path will be used for certificate validation.

Introduced: 4.4.0

Removed: 5.0.0

Default Value: NA

Detail:
**Example:** Dynamically adding or removing URLs is similar to that of regular aerospike nodes. By default, `asinfo -v` displays details only about the node you are connecting to:

```asciidoc
asinfo -v "set-config:context=xdr;dc=DC1;http-url=https://ws1.aerospike.com:2111/index.html;action=add"

asinfo -v "set-config:context=xdr;dc=DC1;http-url=https://ws1.aerospike.com:2111/index.html;action=remove"
```

For the Aerospike Kafka Connector, to display the configured URLs for any node, use the following syntax:

```asciidoc
asinfo -v "get-dc-config"
```

For details about all nodes, use `asadm`:

```asciidoc
asadm -e "enable; asinfo -v get-dc-config"
```

---

#### `http-version`

`enterprise` `dynamic`

Context: xdr

Subcontext: datacenter

Description: This configuration determines the HTTP protocol that talks to the http destination. See [change notification](https://aerospike.com/docs/connectors/streaming/common/change-notification) for further details. Allowed values are:

-   `v1` - Only HTTP v1.1 protocol is used.

Introduced: 4.4.0

Removed: 5.0.0

Default Value: v1

Detail:

---

#### `ignore-bin`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc/namespace

Description: Specifies the name of a bin to exclude from shipping over XDR. You can have multiple `ignore-bin` entries. By default, all bins are shipped. The value of the [`bin-policy`](https://aerospike.com/docs/database/reference/config#xdr__bin-policy) parameter determines if this configuration is honored or not.

For examples, see the [bin policy documentation](https://aerospike.com/docs/database/manage/xdr/bin-policy).

Introduced: 5.0.0

Removed: \-

Default Value: none

Detail:
**Example:**

```asciidoc
xdr {

  dc DC1 {

    node-address-port 10.0.0.1 3000

    namespace nameSpaceName {

       ignore-bin someBinName1

       ignore-bin someBinName2

    }

  }

}
```

Set `ignore-bin` dynamically:

```plaintext
asinfo -v "set-config:context=xdr;dc=DC1;namespace=namespaceName;ignore-bin=binName1"
```

If more than one bin name is passed in asinfo separated by a comma, such as `ignore-bin=binName1,binName2`, it is considered a single bin named `binName1,binName2`.

---

#### `ignore-expunges`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc/namespace

Description: By default, XDR ships user-initiated record deletes. To not ship records deleted by clients, set this parameter `true`.  
  
This parameter only affects non-durable deletes. Durable deletes are always shipped.

Introduced: 5.0.0

Removed: \-

Default Value: false

Detail:
**Example:**

```asciidoc
xdr {

  dc DC1 {

    node-address-port 10.1.0.1 3000

    namespace nameSpaceName {

       ignore-expunges true

    }

  }

}
```

Set `ignore-expunges` dynamically:

```plaintext
asinfo -v "expunges-config:context=xdr;dc=DC1;namespace=namespaceName;ignore-expunges=true"
```

---

#### `ignore-set`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc/namespace

Description: Set-specific parameter to exclude a set from shipping through XDR. You can have multiple `ignore-set` entries.  
  
For more details and examples, see the [set policy documentation](https://aerospike.com/docs/database/manage/xdr/set-policy).

Introduced: 5.0.0

Removed: \-

Default Value: none

Detail:
**Example:**

```asciidoc
xdr {

  dc DC1 {

    node-address-port 10.1.0.1 3000

    namespace nameSpaceName {

       ignore-set someSetName1

       ignore-set someSetName2

    }

  }

}
```

Set `ignore-set` dynamically:

```plaintext
asinfo -v "set-config:context=xdr;dc=DC1;namespace=namespaceName;ignore-set=setName1"
```

If more than one set name is passed in asinfo separated by a comma, such as `ignore-set=setName1,setName2`, it is considered a single set named `setName1,setName2`.

---

#### `max-recoveries-interleaved`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc

Description: Specifies the maximum number of partitions to recover concurrently to provide fairness and prevent partition starvation. In single-threaded interleaved recovery, a thread processes multiple partitions. By default, all pending partitions are partially recovered in a round-robin fashion. This works well when recovery is quick. If recovery for many partitions takes a long time, for example when shipping many records, a partition’s transaction queue may overflow before its recovery is complete. This forces the partition back into recovery. In high-load scenarios, we recommend using this parameter to limit the concurrent recovery to fewer partitions and helping to ensure that their recovery finishes quickly and avoids the overflow cycle.

-   If [`recovery-threads`](https://aerospike.com/docs/database/reference/config#xdr__recovery-threads) is set to 1, `max-recoveries-interleaved` must be 0. \* If `max-recoveries-interleaved` is greater than 0, `recovery-threads` must be 1.

Introduced: 5.5.0

Removed: \-

Default Value: 0

Detail:
**Dynamic configuration constraints:**

-   Switching from parallel to interleaved mode: To enable interleaving when `max-recoveries-interleaved` = 0, first set `recovery-threads` to 1, then change `max-recoveries-interleaved` to the desired value.
    
-   Switching from interleaved to parallel mode: To change `recovery-threads` when `max-recoveries-interleaved` > 0, first set `max-recoveries-interleaved` to 0, then change `recovery-threads` to the desired value.
    

**Example:** Change the parameter dynamically:

```asciidoc
asinfo -v "set-config:context=xdr;dc=DC1;max-recoveries-interleaved=10"
```

---

#### `max-throughput`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc/namespace

Description: Number of records per second to ship using XDR. That is, number of records written per second to the remote datacenters. Setting to 0 will stop throughput. The lowest value for max-throughput is 100. The value for max-throughput can only be in increments of 100. e.g. 100, 200, 1000, etc.

Introduced: 5.0.0

Removed: \-

Default Value: 100000

Detail:
**Example:**

```asciidoc
xdr {

  dc DC1 {

    node-address-port 10.1.0.1 3000

    namespace nameSpaceName {

      max-throughput 50000

    }

  }

}
```

Set `max-throughput` dynamically:

```plaintext
asinfo -v "set-config:context=xdr;dc=DC1;namespace=namespaceName;max-throughput=50000"
```

---

#### `max-used-service-threads`

`enterprise` `dynamic`

Context: xdr

Subcontext: dc

Description: This parameter specifies the number of service threads used by XDR to read records and ship to the destination DC. By default XDR uses all the service threads. Each service thread opens one connection to each destination node. This can lead to lot of connections, especially if the number of service threads are high. This configuration can be used to limit the number of connections made to the destination by limiting the number of service threads used.  
  
Service threads are also used by XDR to read records locally. If this configuration is too low, XDR throughput could be impacted as it may not be able to read enough records in parallel.

Introduced: 5.3.0

Removed: 6.4.0

Default Value: 0

Detail:
Removed in Database 6.4.0. In that version, a partition to service thread affinity is introduced. The number of service threads used by XDR is as follows:

-   For a given partition a service thread is randomly/deterministically assigned (affinity).
-   A given partition will always have one and only one service thread.
-   There cannot be more than one service thread assigned to a partition.
-   There can be more than one partition assigned to a service thread.
-   This also means that it is possible to end up, in some cases, with some service threads having to handle two partitions, some with one and some having none, for the same namespace.

When clusters change, open connections may become idle. Such idle connections will be reaped after 5 minutes.

**Example:** Change the parameter dynamically:

```asciidoc
asinfo -v "set-config:context=xdr;dc=DC1;max-used-service-threads=32"

asinfo -v "set-config:context=xdr;dc=DC1;max-used-service-threads=0"
```

If this configuration value is more than the real number of service threads, all the service threads will be used.

---

#### `namespace`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc

Description: **Note**: this is `namespace` _in the XDR context_, not `namespace` in the namespace context. [Search for `namespace`](https://aerospike.com/docs/database/reference/config#namespace), and look at the **Context** heading to make sure you are working with the correct parameter.  
  
Defines a namespace to be shipped to a remote datacenter over XDR.

-   The parameter must be nested in the [`dc`](https://aerospike.com/docs/database/reference/config#xdr__dc) section of the [`xdr`](https://aerospike.com/docs/database/reference/config#xdr) stanza.
-   The parameter must be followed by a variable name of your choice to refer to the namespace.

For more details, see [Configure XDR](https://aerospike.com/docs/database/manage/xdr/static-xdr).

Introduced: 5.0.0

Removed: \-

Default Value: \-

Detail:
**Example:** Define a namespace to be shipped to a remote datacenter over XDR:

```asciidoc
xdr {

    dc  DataCenter1 {

       namespace someNameSpaceName1 {

         ...

       }

       namespace someNameSpaceName2 {

         ...

       }

    }

}
```

Add a namespace to a datacenter dynamically:

```asciidoc
asinfo -v "set-config:context=xdr;dc=DataCenter1;namespace=someNameSpaceName1;action=add"
```

Remove a namespace from a datacenter dynamically:

```asciidoc
asinfo -v "set-config:context=xdr;dc=DataCenter1;namespace=someNameSpaceName1;action=remove"
```

The namespace definitions in the `dc` section can be in any order, but the variable names of the namespaces must be the same on all nodes involved in XDR.

---

#### `node-address-port`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc

Description: The address and port of a node in the remote datacenter or of a connector. See the [Change Notification Configuration](https://aerospike.com/docs/connectors/streaming/common/change-notification) page for details on how to configure outbound connectors.

Multiple nodes can be specified.

For TLS, an optional tlsname is specified after the port. For details on setting up TLS and `someTlsName`, see [TLS Configuration](https://aerospike.com/docs/database/manage/network/tls).

Introduced: 5.0.0

Removed: \-

Default Value: \-

Detail:
**Example:** Basic XDR stanza in configuration file:

```asciidoc
xdr {

  dc DC1 {

     node-address-port 10.0.0.1 3000 someTlsName1

     node-address-port 10.2.0.1 3000 someTlsName2

     namespace someNameSpace {

       ...

     }

  }

}
```

Add and remove nodes for DC1 dynamically:

```asciidoc
asinfo -v "set-config:context=xdr;dc=DC1;node-address-port=192.168.55.210:3000;action=add"

asinfo -v "set-config:context=xdr;dc=DC1;node-address-port=192.168.55.211:3000;action=remove"
```

IPv6 example:

```asciidoc
asinfo -v "set-config:context=xdr;dc=DC1;node-address-port=[fe80::20c:29ff:fea9:df10]:3000;action=add"

asinfo -v "set-config:context=xdr;dc=DC1;node-address-port=[fe80::20c:29ff:fea9:df10]:3000;action=remove"
```

---

#### `period-ms`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc

Description: The period in milliseconds at which the DC-thread processes partitions for XDR shipment. Decreasing `period-ms` decreases the latency of replication but at the cost of increase in CPU.  
  
For a discussion of the DC and other XDR threads, see [Lifecycle of XDR record shipment with metrics](https://aerospike.com/docs/database/manage/xdr/lifecycle).  
  
Minimum: 5.  
Maximum: 1000.

Introduced: 5.1.0

Removed: \-

Default Value: 100

Detail:
**Example:** Set `period-ms` to 50 milliseconds in configuration file

```asciidoc
xdr {

  dc DC1 {

     period-ms 50

     namespace someNameSpace {

       ...

     }

  }

}
```

Set `period-ms` to 50 dynamically

```asciidoc
asinfo -v "set-config:context=xdr;dc=DC1;period-ms=50"
```

See [What are the different delays affecting an XDR transaction?](https://support.aerospike.com/s/article/What-are-the-different-delays-affecting-an-XDR-transaction) for some of the internal details.

---

#### `recovery-threads`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc

Description: Specifies the number of threads to use for multi-threaded recovery in Aerospike XDR, parallelizing the recovery process by distributing partition scan jobs across multiple threads. The range is 1-32 threads per datacenter. Each recovery thread picks up a partition from the recovery queue and works exclusively on that partition until its recovery is 100% complete. Only after finishing the entire partition does the thread pick up the next partition from the queue. Multiple threads work simultaneously on different partitions, with each thread fully dedicated to one partition at a time.

-   If `recovery-threads` is greater than 1, [`max-recoveries-interleaved`](https://aerospike.com/docs/database/reference/config#xdr__max-recoveries-interleaved) must be 0. \* If`max-recoveries-interleaved` is greater than 0, `recovery-threads` must be 1.

Introduced: 8.1.1

Removed: \-

Default Value: 1

Detail:
**Dynamic configuration constraints:**

-   Switching from parallel to interleaved mode: To enable interleaving when `max-recoveries-interleaved` = 0, first set `recovery-threads` to 1, then change `max-recoveries-interleaved` to the desired value.
    
-   Switching from interleaved to parallel mode: To change `recovery-threads` when `max-recoveries-interleaved` > 0, first set `max-recoveries-interleaved` to 0, then change `recovery-threads` to the desired value.
    

**Example:** Change the parameter dynamically:

```asciidoc
- asinfo -v "set-config:context=xdr;dc=DC1;max-recoveries-interleaved=10"

- asinfo -v "set-config:context=xdr;dc=DC1;recovery-threads=6"
```

---

#### `remote-namespace`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc/namespace

Description: Map a local namespace to a remote namespace with a different name. Set this parameter before connecting to the remote datacenter. Multiple namespaces in the source cluster can ship to the same `remote-namespace`.

Since Database 8.1.0, two source namespaces in a local DC can ship to the same remote namespace, but their set names must be distinct and not overlap.

Prior to Database 8.1.0, the value of `remote-namespace` must be unique across namespaces in the local DC. Two or more namespaces in a cluster cannot map to the same remote namespace, but two different clusters can each map to the same namespace in a third cluster.

Introduced: 5.2.0

Removed: \-

Default Value: none

Detail:
**Example:**

```asciidoc
xdr {

  dc DC1 {

    node-address-port 10.0.0.1 3000

    namespace A {

       remote-namespace B

    }

  }

}
```

Set `remote-namespace` dynamically:

```asciidoc
asinfo -v "set-config:context=xdr;dc=DC1;namespace=A;remote-namespace=B"
```

Use the reserved word `null` to unset `remote-namespace` dynamically:

```asciidoc
asinfo -v "set-config:context=xdr;dc=DC1;namespace=A;remote-namespace=null"
```

If you have already connected to the remote datacenter and encounter difficulties:

-   Disassociate all namespaces in the DC to disconnect existing connections.
-   Set this parameter.
-   Re-add the namespace.

For details see [Dynamic XDR configuration](https://aerospike.com/docs/database/manage/xdr/dynamic-xdr/).

---

#### `sc-replication-wait-ms`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc/namespace

Description: Number of milliseconds that XDR waits before dequeuing a record from the in-memory transaction queue of a namespace configured for Strong Consistency (SC). This gives time for the client-write replicate to finish. With SC, XDR does not ship a record unless the record is successfully replicated.  
  
Setting `sc-replication-wait` too low might cause XDR redundant reads and retries.  
  
Minimum: 5.  
Maximum: 1000.

Introduced: 5.1.0

Removed: \-

Default Value: 100

Detail:
**Example:** Set `sc-replication-wait-ms` to 50 in configuration file:

```asciidoc
xdr {

  dc DC1 {

     node-address-port 10.0.0.1 3000

     namespace someNameSpace {

       sc-replication-wait-ms 50

       ...

     }

  }

}
```

Set `sc-replication-wait-ms` to 50 dynamically:

```asciidoc
asinfo -v "set-config:context=xdr;dc=DC1;namespace=someNameSpace;sc-replication-wait-ms=50"
```

See [What are the different delays affecting an XDR transaction?](https://support.aerospike.com/s/article/What-are-the-different-delays-affecting-an-XDR-transaction) for some of the internal details.

---

#### `ship-bin-luts`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc/namespace

Description: ship-bin-luts is necessary for the XDR bin convergence feature. When this is enabled, XDR ships bin-level last-update-time (LUT). Bin-level LUTs are necessary to determine the winner when trying resolve conflicts in mesh/active-active topologies. Prior to Database 6.3.0, `ship-bin-luts` is not allowed for connectors. See [bin convergence](https://aerospike.com/docs/database/manage/xdr/convergence) for more information.

Introduced: 5.4.0

Removed: \-

Default Value: false

Detail:
**Example:**

```asciidoc
xdr {

  src-id 1

  dc DC1 {

    node-address-port 10.0.0.1 3000

    namespace nameSpaceName {

       bin-policy only-changed

       ship-bin-luts true

    }

  }

}
```

Set `ship-bin-luts` dynamically:

```plaintext
asinfo -v "set-config:context=xdr;dc=DC1;namespace=namespaceName;ship-bin-luts=true"
```

---

#### `ship-bin`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc/namespace

Description: Specifies the name of a bin to ship over XDR. You can have multiple `ship-bin` entries. By default, all bins are shipped. The value of the [`bin-policy`](https://aerospike.com/docs/database/reference/config#xdr__bin-policy) configuration parameter determines if this configuration is honored or not.  
  
For examples, see the [bin policy documentation](https://aerospike.com/docs/database/manage/xdr/bin-policy).

Introduced: 5.0.0

Removed: \-

Default Value: none

Detail:
**Example:**

```asciidoc
xdr {

  dc DC1 {

    node-address-port 10.0.0.1 3000

    namespace nameSpaceName {

       bin-policy changed-and-specified

       ship-bin someBinName1

       ship-bin someBinName2

    }

  }

}
```

Set `ship-bin` dynamically:

```plaintext
asinfo -v "set-config:context=xdr;dc=DC1;namespace=namespaceName;ship-bin=binName1"
```

---

#### `ship-nsup-deletes`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc/namespace

Description: Specifies if XDR ships record deletes from evictions and expirations that are the result of the Namespace Supervisor (nsup). Truncates are not shipped. For more information, see [Namespace Data Retention](https://aerospike.com/docs/database/manage/namespace/retention).

Introduced: 5.0.0

Removed: \-

Default Value: false

Detail:
**Example:**

```asciidoc
xdr {

  dc DC1 {

    node-address-port 10.1.0.1 3000

    namespace nameSpaceName {

       ship-nsup-deletes true

    }

  }

}
```

Set `ship-nsup-deletes` dynamically:

```plaintext
asinfo -v "set-config:context=xdr;dc=DC1;namespace=namespaceName;ship-nsup-deletes=true"
```

When shipping to a [`strong-consistency`](https://aerospike.com/docs/database/reference/config#namespace__strong-consistency) enabled namespace, unless [`strong-consistency-allow-expunge`](https://aerospike.com/docs/database/reference/config#namespace__strong-consistency-allow-expunge) is set to `true`, NSUP deletes shipped using XDR will fail with [`AS_ERR_FAIL_FORBIDDEN`](https://aerospike.com/docs/database/reference/error-codes). This error is reported in the source DC logs as `abandon result 22`.

---

#### `ship-only-specified-bins`

`enterprise` `dynamic`

Context: xdr

Subcontext: dc/namespace

Description: Replaced with the [`bin-policy`](https://aerospike.com/docs/database/reference/config#xdr__bin-policy) configuration parameter in Database 5.2.0 and later.

Introduced: 5.0.0

Removed: 5.2.0

Default Value: false

---

#### `ship-only-specified-sets`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc/namespace

Description: Specifies that XDR should ship only specific sets in a namespace.

For examples, see the [set policy documentation](https://aerospike.com/docs/database/manage/xdr/set-policy).

Introduced: 5.0.0

Removed: \-

Default Value: false

Detail:
This setting should be accompanied at the namespace level with the [`ship-set`](https://aerospike.com/docs/database/reference/config#xdr__ship-set) parameter.

**Example:**

```plaintext
asciidoc

xdr {

  dc DC1 {

    node-address-port 10.0.0.1 3000

    namespace nameSpaceName {

       ship-only-specified-sets true

       ship-set someSetName1

       ship-set someSetName2

    }

  }

}
```

Set `ship-only-specified-sets` dynamically:

```plaintext
asinfo -v "set-config:context=xdr;dc=DC1;namespace=namespaceName;ship-only-specified-sets=true"
```

---

#### `ship-set`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc/namespace

Description: Specifies the name of a set to ship over XDR. You can have multiple `ship-set` entries.

By default, all sets are shipped. To ship only specific sets, use the [`ship-only-specified-sets`](https://aerospike.com/docs/database/reference/config#xdr__ship-only-specified-sets) parameter accompanied by multiple `ship-set` entries for the desired sets to ship.

For more details and examples, see the [set policy documentation](https://aerospike.com/docs/database/manage/xdr/set-policy).

Introduced: 5.0.0

Removed: \-

Default Value: none

Detail:
**Example:**

```asciidoc
xdr {

  dc DC1 {

    node-address-port 10.0.0.1 3000

    namespace nameSpaceName {

       ship-only-specified-sets true

       ship-set someSetName1

       ship-set someSetName2

    }

  }

}
```

Set `ship-set` dynamically:

```plaintext
asinfo -v "set-config:context=xdr;dc=DC1;namespace=namespaceName;ship-set=setName1"
```

---

#### `ship-versions-interval`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc/namespace

Description: A nonzero value that specifies a time window in seconds within which XDR is allowed to skip versions. It is guaranteed that at least one (written) version per time window will be shipped. Allowable range is 1 to 3600 in seconds. Also supports the S,M,H,D suffixes (20M = 20 minutes = 1200 seconds).

Relevant only if [`ship-versions-policy`](https://aerospike.com/docs/database/reference/config#xdr__ship-versions-policy) is true. If set to `0`, every version is shipped.

Introduced: 7.2.0

Removed: \-

Default Value: 60

---

#### `ship-versions-policy`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc/namespace

Description: This policy controls how XDR ships versions of modified records when facing lag between the source cluster and a destination.

-   `latest` continues to ship the most recent version of the record, same as versions earlier than 7.2.
    
-   `interval` attempts to ship at least one version per [`ship-versions-interval`](https://aerospike.com/docs/database/reference/config#xdr__ship-versions-interval) in seconds, otherwise it applies back-pressure by refusing further writes until the record’s current version has shipped.
    
-   `all` confirms that every version of the record reaches the remote destination, and blocks further writes to the record until confirmation.

Introduced: 7.2.0

Removed: \-

Default Value: latest

Detail:
If `ship-versions-policy` is `all`, `delay-ms` must be 0. `delay-ms` cannot exceed the time window specified by `ship-versions-interval`.

---

#### `src-id`

`enterprise` `dynamic` `cloud`

Context: xdr

Description: Allowed values are 0-255. Necessary for the XDR bin convergence feature. Each DC involved in the XDR topology must pick a unique value. Breaks ties that may happen with the bin-level last-update-time. See [bin convergence](https://aerospike.com/docs/database/manage/xdr/convergence) feature.

Introduced: 5.4.0

Removed: \-

Default Value: 0

Detail:
**Example:**

```asciidoc
xdr {

  src-id 1

  dc DC1 {

    node-address-port 10.0.0.1 3000

    namespace nameSpaceName {

       bin-policy only-changed

       ship-bin-luts true

    }

  }

}
```

Set `src-id` dynamically:

```plaintext
asinfo -v "set-config:context=xdr;src-id=1"
```

---

#### `tls-name`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc

Description: This parameter specifies which TLS parameters to use for the specific XDR datacenter TLS connections. The TLS parameters used are configured under the matching [`tls`](https://aerospike.com/docs/database/reference/config#network__tls) sub-stanza. This also implicitly specifies the TLS name the node will present on outgoing XDR client connections. The remote cluster should have a [`tls-authenticate-client`](https://aerospike.com/docs/database/reference/config#network__tls-authenticate-client) directive specifying the same TLS name, or `false`, or `any`. See [TLS name clarification](https://aerospike.com/docs/database/learn/security/tls#tls-name-clarification) for further details.

Introduced: 3.15.0

Removed: \-

Default Value: \-

Detail:
This can either be set to:

-   `CLUSTER_NAME` (literally) which will then pick the cluster-name defined in the Aerospike config file.
    
-   `HOST_NAME` (literally) which will then pick up the hostname from the system.
    
-   User specific where any string can be picked, for example, `my-tls-name`.
    

This should match the certificate as well as what the client will be sending. See the [TLS Guide](https://aerospike.com/docs/database/learn/security/tls) for more information.

**Example:**

```asciidoc
tls-name CLUSTER_NAME

tls-name <hostname>

tls-name my-tls-name
```

It can be set dynamically _only_ when the remote datacenter is not connected and _before_ seed nodes are added. Otherwise, the `asinfo` command will error.

If you have already connected to the remote datacenter and are encountering difficulties, you need to remove the namespaces and seed nodes to disconnect, then set the parameter, and then re-add the seed nodes and namespaces. For details on the necessary `asinfo` commands, see the configuration parameter for [`namespace`](https://aerospike.com/docs/database/reference/config#namespace) in the XDR `dc` subcontext.

---

#### `tls-node`

`enterprise` `static`

Context: xdr

Subcontext: datacenter

Description: The remote cluster’s IP address, tls-name and tls-port number. The TLS name provided through this configuration parameter is the TLS name the cluster node expects the remote DC to present on XDR connections the local node would initiate. See [TLS Name Clarification](https://aerospike.com/docs/database/learn/security/tls#tls-name-clarification) for details.

In Aerospike 5.0.0, superseded by [`node-address-port`](https://aerospike.com/docs/database/reference/config#xdr__node-address-port)

Introduced: 3.1.01.0

Removed: 5.0.0

Default Value: \-

Detail:
**Example:**

```asciidoc
tls-node 192.168.55.210 tls-node1 4000
```

Multiple nodes can be specified. Used as a seed list, similar to `dc-node-address-port` when not using TLS.

---

#### `transaction-queue-limit`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc/namespace

Description: Maximum number of elements allowed in XDR’s in-memory transaction queue per partition, per namespace, per datacenter. Each element is 25 bytes.  
  
Value must be a power of 2 and must be expressed as an integer, not an exponent.  
  
Default: 16\*1024 = 16384.  
Minimum: 1024.  
Maximum: 1048576.

Introduced: 5.0.0

Removed: \-

Default Value: 16384

Detail:
**Example:** Set `transaction-queue-limit` to twice its default value in the configuration file.

```asciidoc
xdr {

    dc dataCenter1 {

        node-address-port someIpAddress1 somePort1

        namespace someNameSpaceName {

        ...

        transaction-queue-limit 32768

        ...

        }

    }

}
```

Set `transaction-queue-limit` dynamically to twice its default value:

```asciidoc
asinfo -v 'set-config:context=xdr;dc=DataCenter1;namespace=someNameSpace;transaction-queue-limit=32768'
```

---

#### `use-alternate-access-address`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc

Description: If `alternate-access-address` is set on the destination nodes, specify `use-alternate-access-address true` at the source nodes in order to use the services-alternate IP addresses to connect to the destination nodes (instead of services). To be used when the remote cluster’s nodes publish IP addresses through [`access-address`](https://aerospike.com/docs/database/reference/config#network__access-address) which are not accessible over WAN and alternate IP addresses accessible over WAN through [`alternate-access-address`](https://aerospike.com/docs/database/reference/config#network__alternate-access-address).

Introduced: 5.0.0

Removed: \-

Default Value: \-

Detail:
**Example:**

```asciidoc
xdr {

  dc DC1 {

    node-address-port 10.1.0.1 3000

    use-alternate-access-address true

    namespace nameSpaceName {

      ...

    }

  }

}
```

Set `use-alternate-access-address` dynamically:

```asciidoc
asinfo -v "set-config:context=xdr;dc=DC1;use-alternate-access-address=true"
```

You should set this parameter _before_ connecting to the remote datacenter. It can be set dynamically _only_ when the remote datacenter is not connected; otherwise, the `asinfo` command will error.

If you have already connected to the remote datacenter and are encountering difficulties, you need to remove the namespace to disconnect, then set the parameter, and then re-add the namespace. For details on the necessary `asinfo` commands, see the configuration parameter for [`namespace`](https://aerospike.com/docs/database/reference/config#namespace) in the XDR `dc` subcontext.

---

#### `write-policy`

`enterprise` `dynamic` `cloud`

Context: xdr

Subcontext: dc/namespace

Description: Determines the behavior of XDR writes on the target datacenter. Allowable values:

-   `auto` (default)
-   `update`
-   `replace`  
      
    Some restrictions apply based on the configured [`bin-policy`](https://aerospike.com/docs/database/reference/config#xdr__bin-policy). See the [write policy documentation](https://aerospike.com/docs/database/manage/xdr/write-policy).

Introduced: 5.1.0

Removed: \-

Default Value: auto

Detail:
**Example:**

```asciidoc
xdr {

  dc DC1 {

    node-address-port 10.1.0.1 3000

    namespace nameSpaceName {

      write-policy replace

      ...

    }

  }

}
```

Set `write-policy` dynamically:

```asciidoc
asinfo -v "set-config:context=xdr;dc=DC1;namespace=nameSpaceName;write-policy=replace"
```

---

#### `xdr-client-threads`

`enterprise` `static`

Context: xdr

Description: Number of threads processing the responses from the destination cluster(s). Replaces `xdr-threads`.

Introduced: 3.8.1

Removed: 5.0.0

Default Value: 3

---

#### `xdr-compression-threshold`

`enterprise` `dynamic`

Context: xdr

Description: In Aerospike 5.0.0, replaced by [`enable-compression`](https://aerospike.com/docs/database/reference/config#xdr__enable-compression). Packet size threshold in bytes beyond which the packets will be compressed. 0 means compression disabled. The compression happens on the XDR read threads, and happens once per DC (the same record will be compressed twice when shipped to 2 different DCs). If CPU seems constrained when compression is enabled, increasing the number of [`xdr-read-threads`](https://aerospike.com/docs/database/reference/config/#xdr__xdr-read-threads) may help.

Introduced: \-

Removed: 5.0.0

Default Value: 0

Detail:
**Example:**

```asciidoc
asinfo -v 'set-config:context=xdr;xdr-compression-threshold=<VALUE>'
```

---

#### `xdr-delete-shipping-enabled`

`enterprise` `dynamic`

Context: xdr

Description: In Aerospike 5.0.0, replaced by [`ignore-expunges`](https://aerospike.com/docs/database/reference/config#xdr__ignore-expunges). This option determines if XDR will ship the deletes of records.

Introduced: \-

Removed: 5.0.0

Default Value: true

Detail:
**Example:** Set `xdr-delete-shipping-enabled` dynamically to false :

```plaintext
asinfo -v "set-config:context=xdr;xdr-delete-shipping-enabled=false"
```

This is honored by ASD and not XDR.

---

#### `xdr-digestlog-iowait-ms`

`enterprise` `dynamic`

Context: xdr

Description: This configuration controls the time, in milliseconds, of 2 different batch/throttling mechanisms around the digestlog io:

-   Time to wait for the queue to be written into the digestlog if the limit of 100 entries has not been reached.
    
-   Time to wait before reading digest log entries from the digest log if the limit of 100 entries has not been reached.

Introduced: 3.13.0.1

Removed: 5.0.0

Default Value: 500

---

#### `xdr-digestlog-path`

`enterprise` `required` `static`

Context: xdr

Description: Path where the digestlog is located. By convention, it is located in `/opt/aerospike/digestlog`. When the XDR process is initially started, it will create a digestlog file of the size specified in the configuration. For example, `xdr-digestlog-path /opt/aerospike/digestlog 100G` will create a digestlog of 100G. Each digestlog entry takes up 80 bytes. Master and prole records end up having entries in the digestlog, but proles will be used only when a node at the source cluster goes down. It is usually fine to have the digestlog on rotational drives as reads from and writes to the digestlog are done in batches of 100.

Introduced: \-

Removed: 5.0.0

Default Value: N/A

Detail:
Changing this size or location requires a restart of the XDR process. In order to modify the digestlog size in a running XDR process, update the configuration, backup or delete the existing digestlog and restart XDR to recreate the digestlog file with the new size.

---

#### `xdr-hotkey-time-ms`

`enterprise` `dynamic`

Context: xdr

Description: Controls how much time (in milliseconds) to wait in between shipping of hot-keys.  
  
In Aerospike Database EE 5.0, replaced by `hot-key-ms`.

Introduced: 3.8.1

Removed: 5.0.0

Default Value: 100

Detail:
**Example:**

```asciidoc
asinfo -v 'set-config:context=xdr;xdr-hotkey-time-ms=<VALUE>'
```

To avoid shipping hotkeys in close succession, XDR maintains a cache for each [`xdr-read-thread`](https://aerospike.com/docs/database/reference/config/#xdr__xdr-read-threads) thread. When a `digest` is read from the`digest log` it is entered into the cache and shipped. The `digest` remains in the cache for `xdr-hotkey-time-ms` If, during that time, the same `digest` is read from the `digest log`, the entry in the cache is marked as ‘dirty’ and the `digest` is not shipped. At the end of `xdr-hotkey-time-ms`, any `digests` marked as dirty are shipped and the dirty flag is removed, the timer is also restarted. If a record does not have the dirty flag, at the end of `xdr-hotkey-time-ms` it is removed from the cache. The net effect is that a frequently updated record will not be shipped more than once every `xdr-hotkey-time-ms` interval.  
Decreasing `xdr-hotkey-time-ms` will increase the frequency by which hotkeys are shipped to destination clusters.

---

#### `xdr-info-timeout`

`enterprise` `dynamic`

Context: xdr

Description: Timeout in millisecond when xdr does info calls. Also used as a time out for remote cluster tending as well.

Introduced: \-

Removed: 5.0.0

Default Value: 10000

Detail:
**Example:**

```asciidoc
asinfo -v 'set-config:context=xdr;xdr-info-timeout=<VALUE>'
```

---

#### `xdr-max-ship-bandwidth`

`enterprise` `dynamic`

Context: xdr

Description: Maximum bandwidth to be used by XDR to ship records to destination clusters.

Introduced: 3.8.1

Removed: 5.0.0

Default Value: 0

Detail:
**Example:**

```asciidoc
asinfo -v 'set-config:context=xdr;xdr-max-ship-bandwidth=<VALUE>'
```

For better result in throttling network traffic to destination clusters, we recommend that you use [`xdr-max-ship-throughput`](https://aerospike.com/docs/database/reference/config#xdr__xdr-max-ship-throughput).

---

#### `xdr-max-ship-throughput`

`enterprise` `dynamic`

Context: xdr

Description: In Aerospike 5.0.0, replaced by [`max-throughput`](https://aerospike.com/docs/database/reference/config#xdr__max-throughput). Maximum throughput of records that are sent to the remote datacenters (number of records written per second to the remote datacenters). This is on a per node basis. 0 means unlimited. In case of shipping to multiple destination clusters, this control the maximum throughput per destination, so the total throughput will be at most the maximum throughput times the number of destination. For example, an `xdr-max-ship-throughput` limit of 1000 when shipping to 3 destination will give a maximum total throughput of 3 x 1000 = 3000.

Introduced: 3.8.1

Removed: 5.0.0

Default Value: 0

Detail:
XDR actually turns this into a maximum number of objects that can be inflight, based on the link latency for a given DC. For example, if a link between 2 DCs has a round trip latency of 10ms, putting 1 record at a time on the link (1 record in flight) would allow for 100 records to be written every second (throughput of 100). In default configuration (no `xdr-max-ship-throughput` set) the derived value for the maximum number of objects that can be in flight at one time is 50000. If the records in flight exceed this value, _XDR_ will start to throttle.

**Example:**

```asciidoc
asinfo -v 'set-config:context=xdr;xdr-max-ship-throughput=<VALUE>'
```

Use this to limit the throughput to the destination clusters. This is useful to prevent flooding the network in case of unexpected backlog of records that suddenly get shipped. For example, temporary connectivity issues to a destination which on restore could overwhelm the network.

---

#### `xdr-min-digestlog-free-pct`

`enterprise` `dynamic`

Context: xdr

Description: Digest log free percentage ([`dlog_free_pct`](https://aerospike.com/docs/database/reference/metrics#xdr__dlog_free_pct)) under which to trigger [`stop_writes`](https://aerospike.com/docs/database/reference/metrics#namespace__stop_writes) and reject application writes. Default value 0 will not disallow writes and will cause older entries in the digest log to be overwritten when the digest log is full. A recommended value to avoid overwriting older entries in the digest log and miss shipping some records would be 5 percent.

Introduced: 3.16.0.1

Removed: 5.0.0

Default Value: \-

Detail:
**Example:** Set `xdr-min-digestlog-free-pct` dynamically to 5%:

```plaintext
asinfo -v "set-config:context=xdr;xdr-min-digestlog-free-pct=5"
```

---

#### `xdr-nsup-deletes-enabled`

`enterprise` `dynamic`

Context: xdr

Description: Replaced in Aerospike 5.0.0 with [`ship-nsup-deletes`](https://aerospike.com/docs/database/reference/config#xdr__ship-nsup-deletes).  
  
This option will determine if XDR will ship deletes which are generated as effect of evictions, expirations or set-delete. Truncates will not be shipped in any case.

Introduced: \-

Removed: 5.0.0

Default Value: false

Detail:
**Example:** Set xdr-nsup-deletes-enabled to true dynamically:

```plaintext
asinfo -v "set-config:context=xdr;xdr-nsup-deletes-enabled=true"
```

This is honored by ASD and not XDR.

---

#### `xdr-read-threads`

`enterprise` `dynamic`

Context: xdr

Description: Number of threads that are used to read from ASD.

Introduced: 3.8.1

Removed: 5.0.0

Default Value: 4

Detail:
**Example:**

```asciidoc
asinfo -v 'set-config:context=xdr;xdr-read-threads=<VALUE>'
```

Dynamically reducing this value may lead to a crash.

---

#### `xdr-ship-bins`

`enterprise` `dynamic`

Context: xdr

Description: By default, XDR will ship the complete record and will replace at destination. Turning `xdr-ship-bins` to true will only ship the modified or new bins in most cases.

Introduced: 3.8.3

Removed: 5.0.0

Default Value: false

Detail:
**Example:** Set xdr-ship-bins to true dynamically:

```plaintext
asinfo -v "set-config:context=xdr;xdr-ship-bins=true"
```

When `xdr-ship-bins` is set to true, only modified or new bins will be shipped to the XDR destination, except in the following cases:

-   Bins were deleted during the write. In this case we need to replace the complete record at the destination.
-   If a local write updates more than 80% of the data in a record, then the complete record is shipped to save a complete record read at the destination.
-   The underlying implementation makes use of a bloom filter which may lead to false positives. In most common cases, though, the probability of a false positive (shipping an extra bin that was not modified) is extremely low (< 0.001 %). Do not hesitate to contact Aerospike for further details regarding specific use cases.
-   If a digest log entry is relogged (due to transient issue when shipping to the destination) the entire record will be shipped upon the subsequent attempt.

---

#### `xdr-shipping-enabled`

`enterprise` `dynamic`

Context: xdr

Description: Enable shipping to remote node while accepting digest logs. Used for suspending shipping.  
Configured DCs that are linked to namespaces will be connected to independently of the value of this setting. To prevent the connections from being made, you will need to either a) [remove all seed nodes](https://aerospike.com/docs/database/reference/config#xdr__dc-node-address-port) from the datacenter definition, or b) [remove the datacenter](https://aerospike.com/docs/database/reference/config#namespace__xdr-remote-datacenter) from all namespace definitions, or do so dynamically to break existing connections.

Introduced: \-

Removed: 5.0.0

Default Value: true

Detail:
**Example:**

```asciidoc
asinfo -v 'set-config:context=xdr;xdr-shipping-enabled=<true | false>'
```

---

#### `xdr-write-timeout`

`enterprise` `dynamic`

Context: xdr

Description: Timeout in millisecond when shipping to destination cluster(s). In case of timeout, digest of the records will be relogged and shipping will be throttled until the destination is marked as down or connectivity is recovered.

Introduced: 3.9.0

Removed: 5.0.0

Default Value: 10000

Detail:
**Example:**

```asciidoc
asinfo -v 'set-config:context=xdr;xdr-write-timeout=<VALUE>'
```

---