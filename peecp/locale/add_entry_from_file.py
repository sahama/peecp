d = []
#
import polib

f = open('list')
for i in f:
    d.append(i.strip())



pot = polib.pofile('peecp.pot')

for i in pot:
    if i.msgid.strip() in d:
        d.remove(i.msgid.strip())
print(d)
for i in d:
    entry = polib.POEntry(msgid=i.strip())
    pot.append(entry)
# pot.save()
pot.save()
# f.close()