# -*- coding: utf-8 -*-
import os
from datetime import datetime
from zoautil_py import datasets
import subprocess

class ZOSNuclearOption:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.uss_temp = f"/tmp/zos_nuke_{self.timestamp}.txt"

    def create_dataset(self, dsn: str, content: str) -> bool:
        """
        Creates a sequential MVS dataset and writes a record to it.
        """
        try:
            # Allocate dataset
            datasets.create(
                dsn,
                type="SEQ",
                primary=1,
                secondary=1,
                record_format="FB",
                record_length=133,
                block_size=29730,
                dataset_type="SEQ",
            )

            # Write content to a temporary USS file
            with open(self.uss_temp, "w") as f:
                f.write(content.ljust(133) + "\n")

            # Copy USS file to MVS dataset
            subprocess.run(["cp", self.uss_temp, f"//'{dsn}'"], check=True)

            # Confirm dataset existence
            if datasets.exists(dsn):
                print(f" {dsn} created and loaded.")
                return True
            else:
                print(f" {dsn} creation failed (not found).")
                return False

        except Exception as e:
            print(f" {dsn} FAILED: {e}")
            return False

    def deploy_payload(self, count=5) -> bool:
        """
        Creates a fleet of datasets with unique names.
        """
        results = []
        for i in range(1, count + 1):
            # Node name must be 8 characters. Keep it short.
            dsn = f"Z47828.ATTACK.GEN{i}"
            content = f"PYTHON NUKE STRIKE #{i} AT {self.timestamp}"
            success = self.create_dataset(dsn, content)
            results.append(success)
        return all(results)


# Run the script
if __name__ == "__main__":
    nuke = ZOSNuclearOption()
    result = nuke.deploy_payload(count=5)
    print("\n Summary:", "ALL SUCCESS " if result else "PARTIAL OR TOTAL FAILURE ")
