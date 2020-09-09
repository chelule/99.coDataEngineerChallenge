# Event Storage
Here we explain tools that can be used for data lake.

## *What Tools could use for data lake. Compare and contrast some existing tools in the market and the factors on which you would decide on a particular one.*


## Data Lake
To use the correct tools, it is required to understand the concept of a Data Lake and it's characteristics. 
- Centralized repository that store structured and unstructured data. 
- Cheap 
- Able to scale at low cost
- Provides some mechanism for data analyst/scientists to relatively explore, analyse and extract the data

Below, comparison of having on-premise(HDFS) and cloud(AWS S3) solution. Factor look into are cost, elasticity, availability and scalability.

## On-Premise vs Cloud
### On-Premise (Running HDFS locally)
- Cost
    - Servers and storage equipment
    - Human cost to maintain. Both hardware and software.
- Elasticity
    - Requires accurate capacity planning resources upfront.
    - Hard to Estimate.
    - Under provision leads to post-hoc provisioning of more resource. 
    - Over provision lead to huge waste due to low utilization.
    - Both under and over provisioning lead to increase of cost.
- Availability
    - Need to manage replication. Having all machines in one location leads to higher probabilities of down time.
    - Having machines in multiple location can increase availability, but also harder to manage. 
- Scalability
    - Buy more hardware. 
    - Manually add and configure servers
- Performance
    - Advantages of data locality. Data is stored and processed on the same machine. Hence access and processing speed are lightning fast.
    - Fast metadata operation
### Cloud (S3)
- Cost
    - Pay exactly what is needed. No need to provision for servers and storage equipment.
    - Do not need a team of Hadoop engineer to main
- Elasticity
    - No need to capacity planning of resources.
    - Only pay what is required.
    - Provider(AWS) automatically provisions resources on demand.
- Availability
    - Provider(AWS) automatically replicates across different data centres. 
    - *Claims* to be 99.999999999% durability and 99.99% availability.
- Scalability
    - Provider(AWS) automatically provisions resources on demand(scaling handle by AWS).
    - There is no need to buy hardware.
- Performance
    - No data locality. Storage and processing is separated. This mean all read need to transfer data over the network.
    - But separation of storage and processing also has their benefits. Larger cluster can be launched for a small period of time to increase throughput, and scale down when processing power is not as demanding(example, adding more spark worker to the cluster when many spark application are in queue, and remove them when many spark worker are idle). 
    
S3 has more advantages compared to on-premise HDFS in terms of cost, elasticity, availability, scalability and performance. Running HDFS on AWS EC2 can improve some of the issue such as buying hardware and maintaining them, but most of the issue still persist in HDFS that is running locally such as elasticity and cost. In this platform evaluation, *S3 is chosen as the data lake*.

### Storing data in s3
- Partition according to predicted/assumed query pattern.
- Store data as parquet for data manipulation and queries.
    - Parquet is columnar. Store data in column rather than row.
    - Self describing. Metadata including schema and structure in each file.
    - Compression. Storing data in column and by partition allows better compression with technique such as dictionary encoding/bit-map run length encoding.
    - Better performance. Analytical query often involved in large number of data (to aggregate and such). With columnar storage, it only need to bring the required compressed columns from disk to memory. This reduce the disk throughput. 
    - For non real-time data analysis, Redshift or Presto can be used to analysis these event data.