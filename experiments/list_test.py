
my_list = ["Nifty Aug 19", "Nifty SEP  19", "NIfty  OcT 19"]

tst_str = "nifty Sep 19"

mnth = tst_str.split()[1].lower()

for i in my_list:
    if mnth in i.lower():
        print (mnth)

