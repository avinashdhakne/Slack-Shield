from Drive import drive
from tqdm import tqdm

class FAT(drive):
    def __init__(self, drive) -> None:
        super().__init__(drive)
        
    
    # Find the cluster having slack spaces i.e. ending cluster of file
    def slacked_clusters(self):

        # starting index of File allocation table
        starting_index_of_FAT = self.index_of_FAT()
        # Ending index of file allocation table
        ending_index_of_FAT = self.index_of_FAT() + (self.sectors_per_FAT() * self.bytes_per_sector())
        self.drive_object.seek(starting_index_of_FAT)
        # List to store the cluster having slack spaces
        slacked_clusters = []
        # Declare current index
        current_index = self.drive_object.tell()

        # Search FAT for clusters having slack spaces 
        # while(current_index < ending_index_of_FAT):
        for current_index in tqdm(range(starting_index_of_FAT, ending_index_of_FAT, 4)):
            FAT_entry = self.drive_object.read(4).hex()
            # print(current_index," < " ,ending_index_of_FAT, FAT_entry ,slacked_clusters)

            # If the cluster is not pointing other cluster 
            if( FAT_entry == "ffffff0f"):
                slacked_cluster_index = int((self.drive_object.tell() - starting_index_of_FAT )/4 -1 )

                # If cluster is in data section
                if(slacked_cluster_index >= 6):
                    slacked_clusters.append(slacked_cluster_index)

            current_index =  self.drive_object.tell()
        return slacked_clusters

if __name__ == "__main__":
    fat = FAT("H")
    
    list = fat.slacked_clusters()
    print(list)
