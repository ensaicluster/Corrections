import os

class Parser:
  def __init__(self, fichier):
    self.proj_name = ""
    self.nb_std_tests = 0
    self.nb_err_tests = 0
    self.tests = list()
    try:
      with open(fichier, 'r') as fd:
        self.lines = fd.readlines()
        self.read = 1
    except:
      print("Erreur: impossible d'ouvrir le fichier correction.")
      self.read = 0
  
  def get_value(self, l):
    current_line = self.lines[l]
    words = current_line.split("=")
    words[1] = words[1].rstrip('\n')
    return(words[1])
  
  def aff_details(self):
    print("#"*50)
    print(" "*(25-(len(self.proj_name)/2))+self.proj_name)
    print("#"*50)
    print("NOTATION : "+str(self.nb_std_tests)+" tests standards, "+str(self.nb_err_tests)+" tests d'erreurs.")    
  
  def start(self):
    if (self.read == 1):
      proj_infos = []
      for i in range(3):
        proj_infos.append(self.get_value(i))
      self.proj_name = proj_infos[0]
      self.nb_std_tests = int(proj_infos[1])
      self.nb_err_tests = int(proj_infos[2])
      for i in range(self.nb_std_tests + self.nb_err_tests):
        self.tests.append(list())
        for j in range(3):
          self.tests[i].append(self.get_value(j+4+(i*3)))
      self.aff_details()

class Test:
  def __init__(self, current_test, test_nb):
    self.test_nb = test_nb
    self.name = current_test[0]
    self.pts = int(current_test[1])
    self.tested_values = current_test[2]
    self.outfile = "out"+str(self.test_nb)
    self.corrfile = "Correction/corrtest"+str(self.test_nb)
    
  def aff_test(self):
    print("_"*50+"\n")
    print("## "+self.name)
    print("## Note sur : "+str(self.pts)+" points")
    print("## Valeurs de test : "+self.tested_values)
    
  def do_test(self):
    pts = 0
    print("Compilation du projet...")
    os.system("gcc -std=c99 Correction/MainTest/main"+str(self.test_nb)+".c *.c")
    print("Ok!\nTesting...")
    os.system("./a.out > "+self.outfile)
    res = os.popen("diff "+self.outfile+" "+self.corrfile).readlines()
    if len(res) == 0:
      print("\033[92m"+"SUCCESS !"+"\033[0m")
      pts += self.pts
      print("Vous avez obtenu "+"\033[92m"+str(self.pts)+" points"+"\033[0m"+".")
    else:
      print("\033[91m"+"FAILURE !"+"\033[0m")
      print("Vous n'avez pas obtenu "+"\033[91m"+str(self.pts)+" points"+"\033[0m"+".")
    return pts

  def start(self):
    self.aff_test()
    return self.do_test()
  
details = Parser("Correction/correction")
details.start()
pts = 0
totalpts = sum(int(details.tests[i][1]) for i in range(details.nb_std_tests + details.nb_err_tests))
print("\n"+"#"*50+"\n"+"TESTS STANDARDS\n"+"#"*50)
for i in range(details.nb_std_tests):
  testing = Test(details.tests[i], i+1)
  pts += testing.start()
if (details.nb_err_tests > 0):
  print("\n"+"#"*50+"\n"+"TESTS DE GESTION D'ERREUR\n"+"#"*50)
  for j in range(i + 1, details.nb_std_tests + details.nb_err_tests):
    testing = Test(details.tests[j], j+1)
    pts += testing.start()
  
print("\n"+"#"*50+"\n"+"NOTE FINALE : "+"\033[36m"+str(pts)+"/"+str(totalpts)+" points"+"\033[0m"+".\n"+"#"*50)