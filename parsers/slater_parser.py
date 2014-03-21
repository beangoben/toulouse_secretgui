#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os
sys.path +=  [ "/home/razoa/CIPSI/EZFIO/Python", "/home/razoa/resultsFile/resultsFile" ]
from ezfio import ezfio

class slater_wraper(object):
	n_list=[]
	l_list=[]
	m_list=[]
	g_list=[]

	m_coef_list=[]
	ao_coef_list=[]
	ao_prim_num_list=[]
	ao_nucl_list=[]

	mo_name=[]
	mo_energy=[]
	mo_occ=[]
	Z=0
	nb_ao=0
	n_act=0


	def __init__(self, path):
		super(slater_wraper, self).__init__()
		self.path=path
		print "we will parse",self.path
		


		self.f=open(path,'r')
		self.contenu = self.f.read().split('\n')

		self.Z=float(self.contenu[0].split()[1].split('=')[1])


		lu_old=6
		
		mo_num_hf_old=0
		
		d = {'s': self.contenu[7].count('s'), 'p': self.contenu[7].count('p')}
		self.mo_name=self.contenu[7].split()

		self.mo_energy=[i for i in self.contenu[8].split() if i != 'ORB.ENERGY']

		for roger in ['s','p']:
			lu=lu_old+1
			mo_num_hf=self.contenu[lu].count(roger)
			
			while (True):
				lu+=1
				l=self.contenu[lu].split()
				if len(l)==0:
					break
			
			for i in range(mo_num_hf):
			    self.m_coef_list.append([])

			while (True):
				try :
					lu+=1
					l=self.contenu[lu].split()
					if len(l)==0:
						break
					else :
						if roger=='s' :
							nb_colone_debut=0
						else :
							nb_colone_debut=mo_num_hf_old+2
			
						nlm=l[nb_colone_debut]
						for i in self.get_nlm(nlm):
							self.n_list.append(i[0])
							self.l_list.append(i[1])
							self.m_list.append(i[2])
							self.g_list.append(float(l[nb_colone_debut+1]))
				
							self.ao_coef_list.append([1.])
							self.ao_prim_num_list.append(1)
							self.ao_nucl_list.append(1)

						for i in self.get_nlm(nlm):

							for i in range(mo_num_hf):
								self.m_coef_list[mo_num_hf_old+i].append(float(l[nb_colone_debut+2+i]))

							break
				except :
				#	raise
					break
		
			mo_num_hf_old=mo_num_hf
		
		nb_mo_s=d['s']
		nb_mo_p=d['p']

		nb_ao_s=len(self.m_coef_list[0])


		try :
			nb_ao_p=len(self.m_coef_list[nb_mo_s])
		except :
			nb_ao_p=0
		
		self.n_act=nb_mo_s+3*nb_mo_p
		self.nb_ao=nb_ao_s+3*nb_ao_p

		nb_ao_sp=nb_ao_s+3*nb_ao_p


		mo_coef_bon=[[] for i in range(nb_ao_sp)]

		#S
		for i in range(nb_mo_s):	
				for j in range(nb_ao_s):
					#print self.m_coef_list[i][j]
					mo_coef_bon[i].append(self.m_coef_list[i][j])
				for j in range(nb_ao_s,self.nb_ao):
					mo_coef_bon[i].append(0.)

		#P
		for i in range(nb_mo_s,nb_mo_s+nb_mo_p,3):
				for j in range(nb_ao_s):
					mo_coef_bon[i].append(0.)


				for j in range(0,nb_ao_p):
					mo_coef_bon[i]+=[self.m_coef_list[i][j],0.,0.]

				mo_coef_bon[i+1] = [0.]+mo_coef_bon[i][:-1]
				mo_coef_bon[i+2] = [0.,0.]+mo_coef_bon[i][:-2]


		a=[0.]*self.nb_ao
		for i in range(nb_mo_s+nb_mo_p+2,nb_ao_sp):
			mo_coef_bon[i]=a

		
		self.m_coef_list=mo_coef_bon
		
		print "nb_ao",self.nb_ao
		print "n_act",self.n_act

		print "n",self.n_list
		print "l",self.l_list
		print "m",self.m_list
		print "g",self.g_list
		
		for i in self.m_coef_list:
			print i


		print "roger"
		print self.ao_prim_num_list

	def get_nlm(self,nlm):
		n=int(nlm[0])
	 	l=nlm[1]
	
	 	if l=='S':
	 		l=0
	 	elif l=='P':
	 		l=1
	
	 	nlm=[]
	 	for i in range(-l,l+1,1):
	 		nlm.append([n,l,i])
	
	 	return nlm	

	def get_mo_name(self):

		dump=self.mo_name
		for i in range(self.n_act,self.nb_ao):
			dump.append('-')

		return dump

	def get_mo_energy(self):
		dump=self.mo_energy
		for i in range(self.n_act,self.nb_ao):
			dump.append('-')
		return self.mo_energy

	def get_mo_occ(self):
		dump=[]
		for i in range( int(self.Z // 2)):
			dump.append('2')

		if ((self.Z%2)==1):
			 dump.append('1')

		for i in range(self.n_act,self.nb_ao):
			dump.append('0')

		return dump
	def get_type_basis(self):
		return "slater"

	def write_ezfio(self,filename):
		ezfio.set_file(filename)
		ezfio.set_ao_basis_used_ao_num(self.nb_ao)
		ezfio.set_ao_basis_slater_ao_num(self.nb_ao) 
		ezfio.set_ao_basis_slater_ao_prim_num(self.ao_prim_num_list)
		ezfio.set_ao_basis_slater_ao_nucl(self.ao_nucl_list)
		
		ezfio.set_ao_basis_slater_ao_n(self.n_list)
		ezfio.set_ao_basis_slater_ao_m(self.m_list)
		ezfio.set_ao_basis_slater_ao_l(self.l_list)
		ezfio.set_ao_basis_slater_ao_gamma(self.g_list)
		ezfio.set_ao_basis_slater_ao_coef(self.ao_coef_list)
		
		ezfio.set_mo_basis_mo_tot_num(self.nb_ao) 
		ezfio.set_mo_basis_mo_coef(self.m_coef_list) 
		
		ezfio.set_nuclei_nucl_num(1)
		ezfio.set_nuclei_nucl_charge([self.Z])
		ezfio.set_nuclei_nucl_coord([0.,0.,0.])
		
		ezfio.set_electrons_elec_beta_num(self.Z // 2)
		ezfio.set_electrons_elec_alpha_num(self.Z // 2 + self.Z % 2)
			
		ezfio.set_parameters_n_act(self.n_act)
		ezfio.set_parameters_n_virt(0)
		ezfio.set_parameters_n_core(0)

if __name__ == '__main__':	
	a=slater_wraper("/home/razoa/work_progress/Slater/data_basis.dat")
	#print a.get_mo_name()
	#print a.get_mo_energy()
	#print a.get_mo_occ()

	a.write_ezfio("/home/razoa/work_progress/Slater/12")
#
#
#f=open("/home/razoa/work_progress/Slater/data_basis.dat",'r')
#
#contenu = f.read().split('\n')


