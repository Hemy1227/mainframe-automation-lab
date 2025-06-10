from zoautil_py.jobs import submit
from datetime import datetime
import tempfile

# Valid JCL string (correct JOB card format)
jcl = """//WSLJCL   JOB (ACCT),'HELLO',CLASS=A,MSGCLASS=A,MSGLEVEL=(1,1)
//STEP1    EXEC PGM=IEBGENER
//SYSPRINT DD SYSOUT=*
//SYSIN    DD DUMMY
//SYSUT1   DD *
HELLO, WORLD
/*
//SYSUT2   DD SYSOUT=*
"""

# Write JCL to a temp file
with tempfile.NamedTemporaryFile(mode="w", delete=False) as jcl_file:
    jcl_file.write(jcl)
    temp_jcl_path = jcl_file.name

# Submit the job
job = submit(temp_jcl_path)
print(f" JOB {job.job_id} submitted at {datetime.now()}")
