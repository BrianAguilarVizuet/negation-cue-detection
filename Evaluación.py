#Sitema de evaluación propuesto:

TrPo = sum(a == b for a, b in zip(reales, pred))
TrNe = sum(a == b == ['O'] * len(b) for a, b in zip(reales, pred))
FaPo = sum(b != a and b == ['O'] * len(b) for a, b in zip(reales, pred)) 
Distintos = sum(a != b for a, b in zip(reales, pred))
TP = TrPo - TrNe
FN = Distintos - FaPo 

#############################
P = (TP)/(TP + FaPo) 
R = (TP)/(TP+FN)
f_1 = (2*P*R)/(P+R)
Acc = (TP+TrNe)/(TP+TrNe+FaPo+FN)

#############################
table = [["Precision",P],["Recall",R],["F1",f_1],["Accuracy",Acc]]
headers = [" ", "CRF"]

print("True Positives(TP) = ",TP) 
print("True Negatives(TN) = ",TrNe) 
print("False Positives(FP) = ",FaPo) 
print("False Negatives(FN) = ",FN) 
print("TOTAL = ",FN+FaPo+TrNe+TP) 
print(tabulate(table, headers, tablefmt="grid"))  