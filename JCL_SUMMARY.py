JCL = """//COPYJOB  JOB (ACCT#),'COPY FILE',CLASS=A,MSGCLASS=X,NOTIFY=&SYSUID
//STEP1    EXEC PGM=IEBGENER
//SYSPRINT DD SYSOUT=*              
//SYSUT1   DD DSN=INPUT.FILE.NAME,DISP=SHR   <-- Input file
//SYSUT2   DD DSN=OUTPUT.FILE.NAME,          <-- Output file
//            DISP=(NEW,CATLG,DELETE),
//            UNIT=SYSDA,
//            SPACE=(TRK,(1,1),RLSE),
//            DCB=(LRECL=80,BLKSIZE=800,RECFM=FB)
//SYSIN    DD DUMMY
"""
# Initialize counters
Job_Statement = 0
EXEC_Statement = 0
DD_Statement = 0
program_name = None  # To store the program name

for line in JCL.splitlines():
    if line.startswith('//') and len(line) >= 14:
        operation_field = line[10:14].strip()
        
        if operation_field == 'JOB':
            Job_Statement += 1
            if 'JOB' in line:
                job_name_start = line.find('JOB') - 4
                job_name_end = line.find(' ', job_name_start)
                if job_name_end == -4:
                    job_name_end = len(line)
                job_name = line[job_name_start:job_name_end].strip()    

        elif operation_field in ('EXEC', 'EXE'):
            EXEC_Statement += 1
            # Extract program name ONLY if PGM= exists
            if 'PGM=' in line:
                pgm_start = line.find('PGM=') + 4  # Start after 'PGM='
                pgm_end = line.find(',', pgm_start)  # End at next comma or line end
                if pgm_end == -1:
                    pgm_end = len(line)
                program_name = line[pgm_start:pgm_end].strip()
        elif operation_field == 'DD':
            DD_Statement += 1

# Print results
if program_name:
    print(f"Program name: {program_name}")  # Only prints IEBGENER
if job_name:
    print(f"Job name: {job_name}")  # Prints the job name if found
print(f"Job statements : {Job_Statement}")
print(f"EXEC Statements: {EXEC_Statement}")
print(f"DD Statements: {DD_Statement}")
