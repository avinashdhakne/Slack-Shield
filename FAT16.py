from drive import Drive
from tqdm import tqdm


class FAT16(Drive):
    def __init__(self, drive) -> None:
        super().__init__(drive)
        self.bytes_per_sector = self.get_bytes_per_sector()
        self.sectors_per_cluster = self.get_sectors_per_cluster()
        self.number_of_FAT = self.get_number_of_FAT()
        self.reserved_sectors = self.get_reserved_sectors()

    # Get the number of entries possible in root directory
    def get_root_entries_FAT16(self):
        self.drive_object.seek(17)
        self.root_entries_FAT16 = int.from_bytes(
            self.drive_object.read(2), "little")
        return self.root_entries_FAT16

    # Find the no of sectors of file allocation table
    def get_sectors_per_FAT_FAT16(self):
        self.drive_object.seek(22)
        self.sectors_per_FAT_FAT16 = int.from_bytes(
            self.drive_object.read(2), "little")
        return self.sectors_per_FAT_FAT16

    # Fine the hidden sectors i.e physical sectors before the drive starts
    def get_hidden_sectors_FAT16(self):
        self.drive_object.seek(28)
        self.hidden_sectors_FAT16 = int.from_bytes(
            self.drive_object.read(4), "little")
        return self.hidden_sectors_FAT16

    def get_index_of_FAT_FAT16(self):
        FAT_index = self.reserved_sectors * self.bytes_per_sector
        self.index_of_FAT_FAT16 = FAT_index
        return self.index_of_FAT_FAT16

    def get_index_of_root_directory_FAT16(self):
        FAT_size = self.sectors_per_FAT_FAT16 * self.bytes_per_sector
        self.index_of_root_directory_FAT16 = (
            FAT_size * 2) + self.index_of_FAT_FAT16
        return self.index_of_root_directory_FAT16

    def get_index_of_first_data_cluster_FAT16(self):
        root_directory_size = self.root_entries_FAT16 * 32
        self.index_of_first_data_cluster_FAT16 = self.index_of_root_directory_FAT16 + \
            root_directory_size
        return self.index_of_first_data_cluster_FAT16

    def get_slacked_clusters_FAT16(self):
        FAT_starting_index = self.index_of_FAT_FAT16
        FAT_ending_index = self.index_of_FAT_FAT16 + \
            self.sectors_per_FAT_FAT16 + self.bytes_per_sector

        self.drive_object.seek(FAT_starting_index)

        slacked_clusters = []

        for current_index in tqdm(range(FAT_starting_index, FAT_ending_index, 4)):
            FAT_entry = self.drive_object.read(2).hex()

            if(FAT_entry == "ffff"):
                slacked_clusters_index = int(
                    (self.drive_object.tell() - FAT_starting_index)/2 - 1)
                if(slacked_clusters_index > 2):
                    slacked_clusters.append(slacked_clusters_index)

        self.slacked_clusters_FAT16 = slacked_clusters
        return self.slacked_clusters_FAT16

    def get_cluster_data_FAT16(self, cluster_index):
        if(cluster_index > 2):
            first_data_cluster = 2
            size_of_a_cluster = self.sectors_per_cluster * self.bytes_per_sector

            cluster_data_index = self.index_of_first_data_cluster_FAT16 + \
                ((cluster_index - first_data_cluster) * size_of_a_cluster)

            self.drive_object.seek(cluster_data_index)
            cluster_data_FAT16 = self.drive_object.read(size_of_a_cluster)
        else:
            raise Exception("Trying to fetch system cluster")
        return cluster_data_FAT16

        # Write the clusters having slack spaces in output file
    def extract_slacked_cluster_FAT16(self):
        slacked_clusters_list = self.slacked_clusters_FAT16
        try:
            file = open("Slack_Spaces_FAT16.txt", "wb+")
            for cluster_index in slacked_clusters_list:
                cluster_data = self.get_cluster_data_FAT16(cluster_index)
                file.write(b"\n\n Data from cluster: " + str(cluster_index).encode() + b"\n\n\n")
                file.write(cluster_data)

        except Exception as e:
            print(e)

        finally:
            print("FAT16 File Has been created...")
            file.close()


if __name__ == "__main__":
    file = FAT16("I")
    print(file.get_reserved_sectors())
    print(file.get_root_entries_FAT16())
    print(file.get_sectors_per_FAT_FAT16())
    print(file.get_hidden_sectors_FAT16())
    print(file.get_index_of_FAT_FAT16())
    print(file.get_index_of_root_directory_FAT16())
    print(file.get_index_of_first_data_cluster_FAT16())
    print(file.get_slacked_clusters_FAT16())
    # print(file.get_cluster_data_FAT16())
    print(file.extract_slacked_cluster_FAT16())
