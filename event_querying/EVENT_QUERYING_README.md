# Event Querying

## What Tools could use for data warehouse. Compare and contrast some existing tools in the market and the factors on which you would decide on a particular one.

## Data Warehouse
To use the correct tools, it is required to understand the concept of a Data Warehouse and it's characteristics. 
- Primarily used by Data Analyst/Business Analyst
- Query are typically very demanding, involves millions of records and aggregating
- Disk bandwidth is often the bottleneck
- Column base storage is suitable for such workload
- Star schema/fact table. Contain lots of columns for flexibility in analytical. 

# What the system wants to achieve
- Perform analysis by Data Analyst/Business Intelligence
- Query a very large data set of events in a responsive way(low latency)

Here we compare 2 columnar database, Redshift and Druid. 

### Druid
- Limited SQL support, specially joins
- Scalable
- Low latency queries
- Real time data ingestion
- Partitioning, data are stored in segments, which are partitioned by time.

### Redshift
- Full SQL support
- Scalable
- Reasonably fast, but slower than Druid
- Batch data ingestion
- Partitioning, data are partition through hashing. Need to re-hash when scaling cluster up/down.


In this scenario, with only considering events data and performing near real-time analysis, Druid would be the better choice. 

On the other hand, Redshift is built for a different purpose. Redshift, and other traditional data warehouse, is more used to perform complex data joins and aggregation. Complex query can involve multiple tables joining together to gather insight. Example do high click on certain property relates to the property distance to the MRT.