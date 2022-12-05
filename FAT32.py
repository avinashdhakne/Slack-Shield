from drive import Drive
from tqdm import tqdm


class FAT32(Drive):
    def __init__(self, drive) -> None:
        super().__init__(drive)
        self.bytes_per_sector = self.get_bytes_per_sector()
        self.sectors_per_cluster = self.get_sectors_per_cluster()
        self.number_of_FAT = self.get_number_of_FAT()
        self.reserved_sectors = self.get_reserved_sectors()

    # Fine the hidden sectors i.e physical sectors before the drive starts
    def get_hidden_sectors_FAT32(self):
        self.drive_object.seek(28)
        self.hidden_sectors_FAT32 = int.from_bytes(
            self.drive_object.read(4), "little")
        return self.hidden_sectors_FAT32

    # Find total sectors in drive
    def get_total_sectors_FAT32(self):
        self.drive_object.seek(32)
        self.total_sectors_FAT32 = int.from_bytes(
            self.drive_object.read(4), "little")
        return self.total_sectors_FAT32

    # Find sectors per File Allocation table
    def get_sectors_per_FAT_FAT32(self):
        self.drive_object.seek(36)
        self.sectors_per_FAT_FAT32 = int.from_bytes(
            self.drive_object.read(4), "little")
        return self.sectors_per_FAT_FAT32

    # Find the Root directory cluster
    def get_root_cluster_FAT32(self):
        self.drive_object.seek(44)
        self.root_cluster_FAT32 = int.from_bytes(
            self.drive_object.read(4), "little")
        return self.root_cluster_FAT32

    # Find the index of file allocation table
    def get_index_of_FAT_FAT32(self):
        self.index_of_FAT_FAT32 = self.reserved_sectors * self.bytes_per_sector
        return self.index_of_FAT_FAT32

    # Find the first index of root directory i.e. cluster 2
    def get_index_of_root_directory_FAT32(self):
        size_of_FAT = self.sectors_per_FAT_FAT32 * \
            self.number_of_FAT * self.bytes_per_sector

        self.index_of_root_directory_FAT32 = self.index_of_FAT_FAT32 + size_of_FAT
        return self.index_of_root_directory_FAT32

    # Find the first file data cluster i.e. cluster 6
    def get_index_of_first_data_cluster_FAT32(self):

        # cluster 2
        size_of_root_directory = self.bytes_per_sector * self.sectors_per_cluster

        # After root directory three clusters are reserved for
        # - WPS setting i.e cluster 3
        # - system volume information i.e. cluster 4
        # - index volume guide i.e. cluster 5
        size_of_reserved_clusters = (
            self.bytes_per_sector * self.sectors_per_cluster) * 3

        self.index_of_first_data_cluster_FAT32 = self.index_of_root_directory_FAT32 + \
            size_of_root_directory + size_of_reserved_clusters

        # First data cluster is cluster 6
        return self.index_of_first_data_cluster_FAT32

    def get_slacked_clusters_FAT32(self):

        starting_index_of_FAT_FAT32 = self.index_of_FAT_FAT32
        ending_index_of_FAT_FAT32 = self.index_of_FAT_FAT32 + (self.sectors_per_FAT_FAT32
                                                               * self.bytes_per_sector)
        self.drive_object.seek(starting_index_of_FAT_FAT32)
        slacked_clusters = []
        # current_index = self.drive_object.tell()

        # Search FAT for clusters having slack spaces
        for current_index in tqdm(range(starting_index_of_FAT_FAT32, ending_index_of_FAT_FAT32, 4)):
            FAT_entry = self.drive_object.read(4).hex()

            # If the cluster is not pointing other cluster
            if(FAT_entry == "ffffff0f"):
                slacked_cluster_index = int(
                    (self.drive_object.tell() - starting_index_of_FAT_FAT32)/4 - 1)

                # If cluster is in data section
                if(slacked_cluster_index >= 6):
                    slacked_clusters.append(slacked_cluster_index)

            # current_index =  self.drive_object.tell()
            self.slacked_clusters_FAT32 = slacked_clusters

        return self.slacked_clusters_FAT32

    # Fetch the cluster data using cluster index
    def get_cluster_data_FAT32(self, cluster_index):
        if(cluster_index >= 6):
            first_data_cluster = 6
            size_of_a_cluster = self.sectors_per_cluster * self.bytes_per_sector

            cluster_data_index = self.index_of_first_data_cluster_FAT32 + \
                ((cluster_index - first_data_cluster) * size_of_a_cluster)

            self.drive_object.seek(cluster_data_index)
            cluster_data_FAT32 = self.drive_object.read(size_of_a_cluster)
        else:
            raise Exception("Trying to fetch system cluster")
        return cluster_data_FAT32

    # Write the clusters having slack spaces in output file
    def extract_slacked_cluster_FAT32(self):
        slacked_clusters_list = self.slacked_clusters_FAT32
        try:
            file = open("Slack_Spaces.txt", "wb+")
            for cluster_index in slacked_clusters_list:
                cluster_data = self.get_cluster_data_FAT32(cluster_index)
                file.write(cluster_data)

        except Exception as e:
            print(e)

        finally:
            print("File Has been created...")
            file.close()


if __name__ == "__main__":
    file = FAT32("H")
    print(file.get_hidden_sectors_FAT32())
    print(file.get_total_sectors_FAT32())
    print(file.get_sectors_per_FAT_FAT32())
    print(file.get_root_cluster_FAT32())
    print(file.get_index_of_FAT_FAT32())
    print(file.get_index_of_root_directory_FAT32())
    print(file.get_index_of_first_data_cluster_FAT32())
    print(file.get_slacked_clusters_FAT32())
    print(file.extract_slacked_cluster_FAT32())
    # print(file.get_cluster_data(8))
