from FAT32 import FAT32
from FAT16 import FAT16


class Main(FAT32, FAT16):
    def __init__(self, drive) -> None:
        super().__init__(drive)

        self.drive_type = self.partition_type(drive)
        print(self.drive_type)

        self.get_reserved_sectors()

        if(self.drive_type == "FAT"):
            # FAT16 functionalities
            self.get_root_entries_FAT16()
            self.get_sectors_per_FAT_FAT16()
            self.get_sectors_per_FAT_FAT16()
            self.get_index_of_FAT_FAT16()
            self.get_index_of_root_directory_FAT16()
            self.get_index_of_first_data_cluster_FAT16()
            self.get_slacked_clusters_FAT16()
            

        elif (self.drive_type == "FAT32"):
            # FAT32 functionalities
            self.get_index_of_FAT_FAT32()
            self.get_sectors_per_FAT_FAT32()
            self.get_index_of_first_data_cluster_FAT32()
            self.get_sectors_per_FAT_FAT32()
            self.get_index_of_FAT_FAT32()
            self.get_slacked_clusters_FAT32()

        else:
            print("Unsupported Disk Type...")

    def get_slack_spaces(self):

        if (self.drive_type == "FAT"):
            self.extract_slacked_cluster_FAT16()

        elif (self.drive_type == "FAT32"):
            self.extract_slacked_cluster_FAT32()

        else:
            print("Disk Type is not supported please try FAT type drive")


if __name__ == "__main__":
    Main("G").get_slack_spaces()
