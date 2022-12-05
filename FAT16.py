from drive import Drive


class FAT16(Drive):
    def __init__(self, drive) -> None:
        super().__init__(drive)
        self.bytes_per_sector = self.get_bytes_per_sector()
        self.sectors_per_cluster = self.get_sectors_per_cluster()
        self.number_of_FAT = self.get_number_of_FAT()

    # Get the number of entries possible in root directory
    def get_root_entries_FAT16(self):
        self.drive_object.seek(17)
        self.root_entries_FAT16 = int.from_bytes(self.drive_object.read(2),"little")
        return self.root_entries_FAT16

    # Find the no of sectors of file allocation table
    def get_sectors_per_FAT_FAT16(self):
        self.drive_object.seek(22)
        self.sectors_per_FAT_FAT16 = int.from_bytes(self.drive_object.read(2),"little")
        return self.sectors_per_FAT_FAT16

    # Fine the hidden sectors i.e physical sectors before the drive starts
    def hidden_sectors_FAT16(self):
        self.drive_object.seek(28)
        self.hidden_sectors_FAT16 = int.from_bytes(self.drive_object.read(4),"little")
        return self.hidden_sectors_FAT16
    
if __name__ == "__main__":
    file = FAT16("I")
    print(file.get_root_entries_FAT16())
    print(file.get_sectors_per_FAT_FAT16())
    print(file.hidden_sectors_FAT16())

    
