from FAT32 import FAT32

class Main(FAT32):
    def __init__(self, drive) -> None:
        super().__init__(drive)
        self.index_of_FAT = self.get_index_of_FAT()
        self.sectors_per_FAT = self.get_sectors_per_FAT()
        self.index_of_root_directory = self.get_index_of_root_directory()
        self.index_of_first_data_cluster = self.get_index_of_first_data_cluster()
        self.sectors_per_FAT = self.get_sectors_per_FAT()
        self.index_of_FAT = self.get_index_of_FAT()
        self.slacked_clusters = self.get_slacked_clusters()

if __name__ == "__main__":
    Main("H").extract_slacked_cluster()
