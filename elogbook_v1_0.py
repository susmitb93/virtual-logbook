from Tkinter import *
import tkFileDialog
import tkMessageBox
import Tkinter as tk
import ScrolledText as scrtxt
import time as T
import os
from os.path import isfile
import shutil


def search_db():
    global src_list;
    src_list = [];
    try:
        F = open(filepath, 'r');
    except:
        print "\n\tCouldn't open log file! :(\n\n";
        return;
    
    srctext = t4.get(); rawtext = F.read(); list2.delete(0, END);
    L = len(rawtext); k = 0; ind1 = 0;
    while True:
        if k==L:
            break;

        if rawtext[k] == chr(4):
            ind2 = k;
            currtext = rawtext[ind1:ind2+1];
            update_list(currtext, srctext);
            ind1 = ind2 + 1;
            #print '\n\tHere: \n'+currtext;

        k = k + 1;




def update_list(s1, s2):
    global src_list;
    str1 = s1.lower(); str2 = s2.lower();
    
    if str1.find(str2) == -1:        
        return;

    k1 = str1.find(chr(3)); str3 = str1[k1+1:]; k2 = str3.find(chr(3));
    strout = str1[k1+1:k2+k1+1]; list2.insert(END, strout);
    src_list.append(s1);    
    



def load_log():
    global src_list; global basepath; global file_list;
    curr_ind = list2.curselection();
    if len(curr_ind) == 0:
        return;
    
    currtext = src_list[curr_ind[0]];
    k1 = currtext.find(chr(3));
    k2 = currtext[k1+1:].find(chr(3)) + k1 + 1;
    k3 = currtext[k2+1:].find(chr(3)) + k2 + 1;
    k4 = currtext[k3+1:].find(chr(3)) + k3 + 1;    
    
    t1.delete(0,END); t1.insert(0, currtext[k1+1:k2]);
    t2.delete(0,END); t2.insert(0, currtext[k2+1:k3]);
    t3.delete(1.0,END); t3.insert(1.0, currtext[k3+1:k4]);
    dirpath = basepath + currtext[:k1]; print dirpath;

    try:
        flist = os.listdir(dirpath); L = len(flist);
        file_list = []; list1.delete(0, END);
        for f_ind in range(L):
            fname = dirpath+'/'+flist[f_ind];
            if isfile(fname):
                file_list.append(fname);
                list1.insert(END, fname);
    except:
        print "\n\n\tCouldn't open additional files...\n";




def save_new():
    global filepath; global basepath; global file_list;
    
    tval0 = T.time(); tval = int(1000 * (tval0 - int(tval0)));
    tempstr0 = T.ctime(); tempstr1 = tempstr0.replace(' ','_'); tempstr = tempstr1.replace(':','_');
    tstamp = str(tval); ch1 = chr(3); ch2 = chr(4);
    tin1 = t1.get(); tin2 = t2.get(); tin3 = t3.get(1.0, END);
    logIDstr = tempstr + "_" + tstamp; dirpath = basepath + logIDstr;    
    try:
        os.mkdir(dirpath);
    except:
        print '\n\tError creating directory!';

    for f_ind in range(len(file_list)):
        try:
            shutil.copy2(file_list[f_ind], dirpath);
        except:
            print '\n\tCould not copy file to log directory! :(\n';

    F = open(filepath, 'a+');
    F.write(logIDstr + ch1 + tin1 + ch1 + tin2 + ch1 + tin3 + ch1 + ch2);
    F.close();

    file_list = [];
    list1.delete(0, END);




def add_file():
    global filepath; global file_list;
    fname = tkFileDialog.askopenfilename();
    if fname == '':
        return;

    file_list.append(fname);
    list1.insert(END, fname);




def remove_file():
    global filepath; global file_list;
    f_ind = list1.curselection();
    if len(f_ind) == 0:
        return;

    retval = file_list.pop(f_ind[0]);
    list1.delete(f_ind[0], f_ind[0]);




def open_file():
    global file_list;
    f_ind = list1.curselection();
    if len(f_ind) == 0:
        return;

    currfile0 = file_list[f_ind[0]]; currfile = currfile0.replace('/','\\');
    os.system("explorer "+currfile);




def quit_all():
    #TBD
    main_win0.destroy();
    exit(0);




main_win0 = Tk();
main_win = Frame(main_win0);

userch = tkMessageBox.askquestion('Initializing', 'Do you already have a logfile?', icon='warning');
if userch=='yes':
    tkMessageBox.showinfo("Initializing...", "Please select logfile");
    fname = tkFileDialog.askopenfilename();
    if fname == '':
        quit_all();
elif userch=='no':
    tkMessageBox.showinfo("Initializing...", "Proceeding to create new logfile...");
    fname = tkFileDialog.asksaveasfilename(initialfile='newlog.flg');
    if fname == '':
        quit_all();

    F = open(fname, 'a+'); F.close();
else:
    quit_all();
    

fname0 = fname[::-1]; tind = fname0.find('/');
path0 = fname0[tind:]; basepath = path0[::-1]; filepath = fname;
src_list = [];
file_list = [];

L1 = Label(main_win, text="Virtual Logbook", font=("Times",25)).grid(row=1, column=2, padx=15, pady=20);
L2 = Label(main_win, text="Title:", font=("Times",20)).grid(row=2, column=1, padx=15, pady=15);
L3 = Label(main_win, text="Short description:", font=("Times",15)).grid(row=3, column=1, padx=15, pady=15);
L4 = Label(main_win, text="Description:", font=("Times",15)).grid(row=4, column=1, padx=15, pady=15);
L5 = Label(main_win, text="Additional files:", font=("Times",15)).grid(row=5, column=1, padx=15, pady=15);
L6 = Label(main_win, text="Search:", font=("Times",15)).grid(row=3, column=6, padx=15, pady=15);

t1 = Entry(main_win); t1.grid(row=2, column=2, padx=5, pady=5); t1.config(font=("Times",15));
t2 = Entry(main_win); t2.grid(row=3, column=2, padx=5, pady=5); t2.config(font=("Times",15));
t3 = scrtxt.ScrolledText(master = main_win, wrap = tk.WORD, width = 40, height = 10);
t3.grid(row=4, column=2, padx=15, pady=15); t3.config(font=("Times",12));
t4 = Entry(main_win); t4.grid(row=3, column=7, padx=20, pady=5); t4.config(font=("Times",10));

list1 = Listbox(master=main_win, width=50, height=10); list1.grid(row=5, column=2, rowspan=3, padx=5, pady=15); list1.config(font=("Times",10));
list2 = Listbox(master=main_win, width=30, height=15); list2.grid(row=4, column=7, padx=15, pady=15); list2.config(font=("Times",10));

b1 = Button(main_win, text='Find', font=("Times",12), bg='white', command=search_db);
b1.grid(row=3, column=8, padx=15, pady=5);

b2 = Button(main_win, text='Load', font=("Times",12), bg='white', command=load_log);
b2.grid(row=4, column=8, padx=15, pady=5);

b3 = Button(main_win, text='Save', font=("Times",15), bg='white', command=save_new);
b3.grid(row=8, column=2, padx=20, pady=20);

b4 = Button(main_win, text='Quit', font=("Times",15), bg='white', command=quit_all);
b4.grid(row=8, column=7, padx=20, pady=20);

b5 = Button(main_win, text='Add', font=("Times",12), bg='white', command=add_file);
b5.grid(row=5, column=4, padx=5, pady=5);

b6 = Button(main_win, text='Remove', font=("Times",12), bg='white', command=remove_file);
b6.grid(row=6, column=4, padx=5, pady=5);

b7 = Button(main_win, text='Open', font=("Times",12), bg='white', command=open_file);
b7.grid(row=7, column=4, padx=5, pady=5);

main_win.pack(); main_win0.update_idletasks();
main_win0.minsize(main_win.winfo_reqwidth(), main_win.winfo_reqheight());
main_win0.maxsize(main_win.winfo_reqwidth(), main_win.winfo_reqheight());
main_win0.mainloop();
