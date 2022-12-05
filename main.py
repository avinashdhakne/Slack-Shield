from FAT32 import FAT32
from FAT16 import FAT16

class Main(FAT32, FAT16):
    def __init__(self, drive) -> None:
        super().__init__(drive)
        self.index_of_FAT = self.get_index_of_FAT_FAT32()
        self.sectors_per_FAT = self.get_sectors_per_FAT_FAT32()
        self.index_of_root_directory = self.get_index_of_root_directory_FAT32()
        self.index_of_first_data_cluster = self.get_index_of_first_data_cluster_FAT32()
        self.sectors_per_FAT = self.get_sectors_per_FAT_FAT32()
        self.index_of_FAT = self.get_index_of_FAT_FAT32()
        self.slacked_clusters = self.get_slacked_clusters_FAT32()

if __name__ == "__main__":

    Main("H").extract_slacked_cluster_FAT32()
