from ebaysdk.trading import Connection as Trading
try:    
    api = Trading(appid="SyedHuss-b18a-4e63-84e5-5bdc5dae3942", devid="88b30cf5-7e11-4b47-839d-0fadc366e078", certid="6b1636d9-bc74-4c5a-a9df-38dd8fd86b7f", token="AgAAAA**AQAAAA**aAAAAA**7t94Vg**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6AHlYqoCJaBow6dj6x9nY+seQ**kx0DAA**AAMAAA**+kgOSfQxX3bIcIWkrkncbP/fJmL8ikWpMlAvOm0WbyPNDUCakunumbeQmvct0j8MPdy7W8VesNNDP0jl0t9RvoBXJX0MoHvRo8utnDhx10x8OYSUWk4ON/IdfpuI+L3C+9c4P88y1D4WQZStQJjRzFl+/J7J0kiLZTbItj9gY4VKJfRowS46KM/WUMX4bB9NXlJMaQ+tmGahQdvsv3T8Cmue+2+ZM+ruaWGxRDJfimwM03e14jhgC2OFnOCXPiDsFClryPIEeagq0WlJQ9F2v6P/18SBTCveskvvbEfieujOr62eE44c7iGMLCr+NewMyYeXm9wTC2GZnPHTPme6Tw2SB5L8z4YnszaA3CKOKqv75ploX4YHIX8c1bXxdPuc3Zq0XtB0U+x4ZU5iMjMYj0UZ9aJWhPzPLE1j+TCVDlhL+ut1glxzQi7x8wn4qnI+ajFz+SYLJkWvF2xL6RbGxc34KKGuKSv5P8fNH3+/wBw7K98DgEbMKurCAfrGTy76Wedyz1e02tT5kMufsrO840x2vZBSXqqLwPxy00wEem/4sbeeFi9r8hizdBels+O5dKB9z3jURVWwNJ8ydRxAEBqpN5nSzf7BtTrIWEINnSiRB9A61SIsXivInD+HPjeBTAMZlBiJT04ZtloxiQS0+KnAW8Plgof1ylBLWS6yspH8Fdv69xDXrLDC9t9Vtp/qs6ay96ES0CalSzHhKBt4oJW6NtoFDhlSMF2Y5ahqQ3d67CAvnYlVE1gHAkKb4ror")
    response = api.execute('GetMyeBaySelling', {'SoldList': {'DurationInDays' : '1'}})
    print(response.dict())
    print(response.reply)
except ConnectionError as e:
    print(e)
    print(e.response.dict())

