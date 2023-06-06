class DaftarKlien:
    def __init__(self):
        self.id_berdasarkan_socket = {}
        self.socket_berdasarkan_id = {}
        
    def tambah_socket(self, io_stream) -> None:
        self.id_berdasarkan_socket[io_stream] = None
        
    def hapus_socket(self, io_stream) -> None:
        id_user = self.id_berdasarkan_socket.get(io_stream)
        
        try:
            self.id_berdasarkan_socket.pop(io_stream)
            if id_user is not None:
                self.socket_berdasarkan_id.pop(id_user)
        
        except Exception as e:
            pass
        
    def pasangkan_user_dengan_socket(self, id_user : str, io_stream):
        try :
            self.id_berdasarkan_socket[io_stream] = id_user
            self.socket_berdasarkan_id[id_user] = io_stream
        except Exception as e:
            pass
        
    def hapus_pasangan_user_dengan_socket(self, io_stream):
        try :
            id_user = self.id_berdasarkan_socket[io_stream]
            self.id_berdasarkan_socket[io_stream] = None
            
            self.socket_berdasarkan_id.pop(id_user)
        except Exception as e:
            pass
                
    def dapatkan_socket_berdasarkan_id(self, id_user : str):
        return self.socket_berdasarkan_id.get(id_user)
        