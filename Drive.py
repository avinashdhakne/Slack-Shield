from System import system

class drive(system):

    def __init__(self, drive) -> None:
        super().__init__()

        # Get the drive path
        self.drive_path = "\\\\.\\" + drive + ":"

        # Open the drive for operations
        try:
            self.drive_object = open(self.drive_path, "rb+")
            print(f"Drive \"{drive}\" is ready fo forensics...")
            self.drive_object.read(10)
        except Exception as e:
            print(e)

    # Find the bytes per sector in drive
    def bytes_per_sector(self):
        self.drive_object.seek(11)
        return int.from_bytes(self.drive_object.read(2), "little")

    # Find the sectors per cluster in drive
    def sectors_per_cluster(self):
        self.drive_object.seek(13)
        return int.from_bytes(self.drive_object.read(1), "little")

    # Find the reserved sectors in the drive
    def reserved_secotrs(self):
        self.drive_object.seek(14)
        return int.from_bytes(self.drive_object.read(2), "little")

    # Find the number of File allocation table in drive
    def number_of_FAT(self):
        self.drive_object.seek(16)
        return int.from_bytes(self.drive_object.read(1), "little")

    # Fine the hidden sectors i.e physical sectors before the drive starts
    def hidden_sectors(self):
        self.drive_object.seek(28)
        return int.from_bytes(self.drive_object.read(4), "little")

    # Find total sectors in drive
    def total_sectors(self):
        self.drive_object.seek(32)
        return int.from_bytes(self.drive_object.read(4), "little")

    # Find sectors per File Allocation table
    def sectors_per_FAT(self):
        self.drive_object.seek(36)
        return int.from_bytes(self.drive_object.read(4), "little")

    # Find the Root dirctry cluster
    def root_cluster(self):
        self.drive_object.seek(44)
        return int.from_bytes(self.drive_object.read(4), "little")

    # Find the index of file allocation table
    def index_of_FAT(self):
        return self.reserved_secotrs() * self.bytes_per_sector()

    # Find the first index of root directry i.e. cluster 2
    def index_of_root_directry(self):
        FAT_bytes = self.sectors_per_FAT() * self.number_of_FAT() * \
            self.bytes_per_sector()
        return self.index_of_FAT() + FAT_bytes

    # Find the first file data cluster i.e. cluster 6
    def first_data_cluster(self):

        # cluster 2
        size_of_root_directory = self.bytes_per_sector() * self.sectors_per_cluster()

        # After root dirctory three clusters are reserved for
        # - WPS setting i.e cluater 3
        # - system volume information i.e. cluster 4
        # - index volume guide i.e. cluater 5
        size_of_reserved_clusters = (self.sectors_per_cluster() * self.bytes_per_sector()) * 3

        # First data cluster is cluster 6
        return self.index_of_root_directry() + size_of_root_directory + size_of_reserved_clusters


if __name__ == "__main__":
    file = drive("H")
    print(file.bytes_per_sector())
    print(file.sectors_per_cluster())
    print(file.reserved_secotrs())
    print(file.number_of_FAT())
    print(file.hidden_sectors())
    print(file.total_sectors())
    print(file.sectors_per_FAT())
    print(file.root_cluster())
    print(file.index_of_FAT())
    print(file.index_of_root_directry())
    print(file.first_data_cluster())
