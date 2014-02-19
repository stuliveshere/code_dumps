class Tree(Frame):
    '''directory tree browser'''
    def __init__(self, master, path):
        Frame.__init__(self, master)
        self.tree = Treeview(self)
        ysb = Scrollbar(self, orient='vertical', command=self.tree.yview)
        xsb = Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.heading('#0', text='Select New Database', anchor='center')
        abspath = os.path.abspath(path)
        root_node = self.tree.insert('', 'end', text=abspath, open=True)
        self.process_directory(root_node, abspath)
        self.tree.pack(fill='both', expand=Y, padx=5, pady=5)
        self.pack(fill='both', expand=Y, padx=5, pady=5)

    def process_directory(self, parent, path):
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            isdir = os.path.isdir(abspath)
            oid = self.tree.insert(parent, 'end', text=p, open=False)
            if isdir:
                self.process_directory(oid, abspath)

class NewFile(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        # Create widgets
        self.v = StringVar()
        self.e = Entry(self, textvariable=self.v)
        self.e.pack(side=LEFT, expand=Y, fill=X)
        self.buttonB = Button(self, text="create",)
        self.buttonB.pack(side=RIGHT,)
        self.pack(fill=X, expand=N, padx=5, pady=5)
        
        
    def new_db_wizard(self):
        '''top level view for new database wizard'''
        self.wroot = Toplevel()
        self.wroot.title('New Database Wizard')
        self.wroot.geometry("400x600")
        self.wizard = Wizard(master=self.wroot, npages=2)
        self.pagelist = []
        self.pagelist.append(Label(self.wizard.page_container(0), text='Create new database file'))
        self.pagelist[0].pack(side=TOP)
        self.pagelist.append(NewFile(self.wizard.page_container(0)))
        self.pagelist.append(Tree(self.wizard.page_container(0), '../'))
        for page in self.pagelist: self.wizard.add_page_body(page)
        self.wizard.pack(fill='both', expand=True)