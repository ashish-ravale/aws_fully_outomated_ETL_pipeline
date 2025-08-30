import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import functions as SqlFuncs

# ✅ Accept parameters from Lambda
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'input_path', 'output_path'])

input_path = args['input_path']
output_path = args['output_path']

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read only the uploaded file
input_df = glueContext.create_dynamic_frame.from_options(
    format_options={"quoteChar": "\"", "withHeader": True, "separator": ","},
    connection_type="s3",
    format="csv",
    connection_options={"paths": [input_path]},   # only the passed file
    transformation_ctx="source"
)

# Drop duplicates
dedup_df = DynamicFrame.fromDF(input_df.toDF().dropDuplicates(), glueContext, "dedup")

# Example: drop null columns
clean_df = DropNullFields.apply(frame=dedup_df, transformation_ctx="clean")

# Write to output folder
glueContext.write_dynamic_frame.from_options(
    frame=clean_df,
    connection_type="s3",
    format="csv",
    connection_options={"path": output_path, "partitionKeys": []},
    transformation_ctx="target"
)

job.commit()
