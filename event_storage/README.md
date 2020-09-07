# Event Storage
Here we explain tools that can be used for data lake.

## Data Lake
To use the correct tools, it is required to understand the concept of a Data Lake and it's characteristics. 
- Centralized repository that store structured and unstructured data. 
- Cheap 
- Able to scale at low cost
- Provides some mechanism for data analyst/scientists to relatively explore, analyse and extract the data
## Local vs Cloud
### Local (HDFS)
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

    
