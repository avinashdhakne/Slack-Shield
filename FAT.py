from Drive import drive
class FAT(drive):
    def __init__(self, drive) -> None:
        super().__init__(drive)
        
    def slacked_clusters(self):
        # statring index of File allocation table
        statring_index_of_FAT = self.index_of_FAT()

        # Ending index of file allocation table
        ending_index_of_FAT = self.index_of_FAT() + (self.sectors_per_FAT() * self.bytes_per_sector())
        print(statring_index_of_FAT)

        self.drive_object.seek(statring_index_of_FAT)
        print(self.drive_object.tell())

        # as first two entries i.e. 8 bytes are reserved hence we will not consider them 
        slacked_clusters = []
    
        current_index = self.drive_object.tell()

    
        # while(current_index < ending_index_of_FAT):
        for i in range(20):
            FAT_entry = self.drive_object.read(4).hex()
            print(current_index," < " ,ending_index_of_FAT, FAT_entry ,slacked_clusters)
            # print(FAT_entry)
            if( FAT_entry == "ffffff0f"):
                slacked_cluster_index = int((self.drive_object.tell() - statring_index_of_FAT )/4 -1 )
                if(slacked_cluster_index >= 6):
                    slacked_clusters.append(slacked_cluster_index)

            current_index =  self.drive_object.tell()
                
        
        return slacked_clusters


        # while(self.drive_object.read(4) != )

if __name__ == "__main__":
    fat = FAT("H")
    
    list = fat.slacked_clusters()
    print(list)

    # file = FAT("H")
    # print(file.bytes_per_sector())
    # print(file.sectors_per_cluster())
    # print(file.reserved_secotrs())
    # print(file.number_of_FAT())
    # print(file.hidden_sectors())
    # print(file.total_sectors())
    # print(file.sectors_per_FAT())
    # print(file.root_cluster())
    # print(file.index_of_FAT())
    # print(file.index_of_root_directry())
    # print(file.first_data_cluster())