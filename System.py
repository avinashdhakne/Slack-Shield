import psutil

class system:
    def __init__(self) -> None:
        pass

    def partition_type(self):
        for partition in psutil.disk_partitions():
            print("Partition: " + partition.mountpoint, "Type: ",
                  partition.fstype, partition.opts.split(",")[1])

    def partition_memory_status(self):
        for partition in psutil.disk_partitions():
            partition_data = psutil.disk_usage(partition.mountpoint)
            print("Partition: ", partition.mountpoint,
                  "Total Memory: ", partition_data.total)

            bar = "█" * int(partition_data.percent) + "-" * \
                (100-int(partition_data.percent))

            print(f"|{bar}| Used: { partition_data.percent }%", end="\n\n")


if __name__ == "__main__":
    sys = system()
    sys.partition_type()
    sys.partition_memory_status()
