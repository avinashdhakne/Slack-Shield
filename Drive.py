import psutil


class Drive:
    def __init__(self, drive) -> None:
        # Get the drive path
        self.drive_path = "\\\\.\\" + drive + ":"

        # Open the drive for operations
        try:
            self.drive_object = open(self.drive_path, "rb+")
            print(f"Drive \"{drive}\" is ready fo forensics...")
            self.drive_object.read(10)
        except Exception as e:
            print(e)

     # Get the details of available partitions
    def partition_details(self):
        for partition in psutil.disk_partitions():
            print("Partition: " + partition.mountpoint, "Type: ",
                  partition.fstype, partition.opts.split(",")[1])

    # Get the partition type by its mount-point
    def partition_type(self, partition):
        partition_path = partition + ":\\"
        partition_types = {}
        for partition in psutil.disk_partitions():
            partition_types.update({partition.mountpoint: partition.fstype})

        return partition_types[partition_path]

    # Get the memory status of partition
    def partition_memory_status(self):
        for partition in psutil.disk_partitions():
            partition_data = psutil.disk_usage(partition.mountpoint)
            print("Partition: ", partition.mountpoint,
                  "Total Memory: ", partition_data.total)

            bar = "█" * int((partition_data.percent/2)) + "-" * \
                int((100 - partition_data.percent)/2)

            print(f"|{bar}| Used: { partition_data.percent }%", end="\n\n")

        # Find the bytes per sector in drive
    def get_bytes_per_sector(self):
        self.drive_object.seek(11)
        self.bytes_per_sector = int.from_bytes(
            self.drive_object.read(2), "little")
        return self.bytes_per_sector

    # Find the sectors per cluster in drive
    def get_sectors_per_cluster(self):
        self.drive_object.seek(13)
        self.sectors_per_cluster = int.from_bytes(
            self.drive_object.read(1), "little")
        return self.sectors_per_cluster

    # Find the reserved sectors in the drive
    def get_reserved_sectors(self):
        self.drive_object.seek(14)
        self.reserved_sectors = int.from_bytes(
            self.drive_object.read(2), "little")
        return self.reserved_sectors

    # Find the number of File allocation table in drive
    def get_number_of_FAT(self):
        self.drive_object.seek(16)
        self.number_of_FAT = int.from_bytes(
            self.drive_object.read(1), "little")
        return self.number_of_FAT

    # Get the volume name of the partition
    def get_volume_name(self):
        self.drive_object.seek(43)
        self.volume_name = self.drive_object.read(11).decode()
        return self.volume_name

    # Get the file system of the partition
    def get_file_system(self):
        self.drive_object.seek(54)
        self.file_system = self.drive_object.read(8).decode()
        return self.file_system


if __name__ == "__main__":
    sys = Drive("H")
    print(sys.partition_type("C"))
    print("\n\n\n")
    sys.partition_memory_status()
    print("\n\n\n")
    sys.partition_details()

    file = Drive("I")
    print(file.get_bytes_per_sector())
    print(file.get_sectors_per_cluster())
    print(file.get_reserved_sectors())
    print(file.get_number_of_FAT())
    print(file.get_file_system())
    print(file.get_volume_name())
