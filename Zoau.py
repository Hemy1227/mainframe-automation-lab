from zoautil_py import MVSCmd, Datasets, Jobs
from zoautil_py.types import DDStatement
from zoautil_py.utils import get_job_name, get_job_id, get_job_status, get_job_info
from zoautil_py.utils import get_dataset_info, get_dataset_member_info, get_dataset_members
import io
import sys
# Define dataset name and temporary dataset for output
temp_dataset = f"{get_job_name()}.TEMP.DATA"
pds_name = "YOUR.PDS.NAME"

# Demonstrate dataset operations
def dataset_operations():
    # Create a new dataset
    Datasets.create(temp_dataset, "PS", dcb="RECFM=FB,LRECL=80,BLKSIZE=27920")
    
    # Write content to dataset
    Datasets.write(temp_dataset, ["This is a test line", "Another line"])
    
    # Read dataset content
    content = Datasets.read(temp_dataset)
    print("Dataset content:", content)
    
    # Get dataset information
    info = get_dataset_info(temp_dataset)
    print("Dataset info:", info)

# Demonstrate job submission
def submit_job():
    # Create DD statements
    dd_statements = [
        DDStatement("SYSUT1", temp_dataset),
        DDStatement("SYSUT2", "&&TEMP")
    ]
    
    # Submit a job with JCL
    job_id = Jobs.submit("""//COPYJOB JOB (),'COPY',MSGCLASS=H
//STEP1    EXEC PGM=IEBGENER""", dd_statements)
    
    # Monitor job status
    status = get_job_status(job_id)
    print(f"Job {job_id} status: {status}")
    
    # Get detailed job info
    job_info = get_job_info(job_id)
    print("Job info:", job_info)

# Execute MVS commands
def execute_mvs_commands():
    # Issue MVS command
    result = MVSCmd.execute('D A,L')
    print("MVS command output:", result)

if __name__ == "__main__":
    dataset_operations()
    submit_job()
    execute_mvs_commands()
    # Demonstrate PDS operations
    def pds_operations():
        # Create a partitioned dataset
        Datasets.create(pds_name, "PDS", dcb="RECFM=FB,LRECL=80,BLKSIZE=27920")
        
        # Write to a member
        Datasets.write(f"{pds_name}(MEMBER1)", ["Member 1 content"])
        
        # List members
        members = get_dataset_members(pds_name)
        print("PDS members:", members)
        
        # Get member info
        member_info = get_dataset_member_info(f"{pds_name}(MEMBER1)")
        print("Member info:", member_info)

    # Demonstrate dataset deletion
    def cleanup_operations():
        # Delete temporary dataset
        if Datasets.exists(temp_dataset):
            Datasets.delete(temp_dataset)
        
        # Delete PDS
        if Datasets.exists(pds_name):
            Datasets.delete(pds_name)

    # Add new operations to main
    if __name__ == "__main__":
        dataset_operations()
        pds_operations()
        submit_job()
        execute_mvs_commands()
        cleanup_operations()
        def additional_mvs_commands():
            # Display system information
            system_info = MVSCmd.execute('D M=CPU')
            print("CPU info:", system_info)
            
            # Display active jobs
            active_jobs = MVSCmd.execute('D A,ALL')
            print("Active jobs:", active_jobs)
            
            # Display time and date
            time_info = MVSCmd.execute('D T')
            print("System time:", time_info)
            
            # Display page dataset status
            page_info = MVSCmd.execute('D ASM')
            print("Page dataset status:", page_info)
            
            # Display channel path status
            path_info = MVSCmd.execute('D M=CHP')
            print("Channel paths:", path_info)

        if __name__ == "__main__":
            additional_mvs_commands()
def display_dataset_info():
    try:
        # Display dataset information
        dataset_info = MVSCmd.execute('D U,DASD')  # Display DASD units
        print("DASD information:", dataset_info)
        
        # List catalog contents
        catalog_info = MVSCmd.execute('LISTCAT')
        print("Catalog entries:", catalog_info)
        
        # Display specific dataset
        ds_info = MVSCmd.execute('D SMS,DSNAME=your.dataset.name')
        print("Dataset status:", ds_info)
    
    except Exception as e:
        print(f"Error executing commands: {e}")

if __name__ == "__main__":
    # Create a temporary dataset for output if it doesn't exist
    output_dataset = f"{get_job_name()}.OUTPUT.DATA"
    if not Datasets.exists(output_dataset):
        Datasets.create(output_dataset, "PS", dcb="RECFM=FB,LRECL=133,BLKSIZE=27930")
    
    # Redirect standard output to collect the information
    output = io.StringIO()
    sys.stdout = output
    
    # Run the display function
    display_dataset_info()
    
    # Restore standard output
    sys.stdout = sys.__stdout__
    
    # Write captured output to dataset
    Datasets.write(output_dataset, output.getvalue().splitlines())
    print(f"Results have been written to {output_dataset}")
    
    print("\nSummary of Functions and Utilities Used:")
    print("\n1. Dataset Operations:")
    print("- Datasets.create(): Creates new datasets")
    print("- Datasets.write(): Writes content to datasets")
    print("- Datasets.read(): Reads dataset content")
    print("- Datasets.exists(): Checks if dataset exists")
    print("- Datasets.delete(): Deletes datasets")
    
    print("\n2. Job Operations:")
    print("- Jobs.submit(): Submits JCL jobs")
    print("- get_job_status(): Monitors job status")
    print("- get_job_info(): Gets detailed job information")
    print("- get_job_name(): Gets current job name")
    print("- get_job_id(): Gets job ID")
    
    print("\n3. MVS Command Operations:")
    print("- MVSCmd.execute(): Executes MVS commands")
    print("Commands used:")
    print("  - D A,L: Display active jobs")
    print("  - D M=CPU: Display CPU information")
    print("  - D A,ALL: Display all active jobs")
    print("  - D T: Display time and date")
    print("  - D ASM: Display page dataset status")
    print("  - D M=CHP: Display channel paths")
    print("  - D U,DASD: Display DASD units")
    print("  - LISTCAT: List catalog entries")
    print("  - D SMS,DSNAME: Display SMS dataset info")
    
    print("\n4. PDS Operations:")
    print("- get_dataset_members(): Lists PDS members")
    print("- get_dataset_member_info(): Gets member information")
    print("- get_dataset_info(): Gets dataset information")

