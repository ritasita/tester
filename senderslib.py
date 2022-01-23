from time import time
from numpy import *
from pickle import dump,load

def powing(n,s):
    ans=[]
    while n>0:
        ans.append(s[n%len(s)])
        n//=len(s)
    ans=ans[::-1]
    if type(s)==str:
        return ''.join(ans)
    return ans

class Connection:
	def __init__(self,key=None):
		self.key=key
		self.modR=2**127-1
		if self.key==None:
			self.key=self.microrand(int(time()*100000))

	def microrand(self,a):
		return pow(51,self.modR-pow(51,a,self.modR)-1,self.modR)

	def gethash(self,s):
		a=1
		for x in s:
			a+=ord(x)
			a=self.microrand(a)
		return self.microrand(a)

	def encodemix(self,a,key):
		b=[x for x in a]
		for x in range(len(b)):
			key=self.microrand(key)
			r1=key%(len(b)-x)+x
			b[x],b[r1]=b[r1],b[x]
		return ''.join(b)

	def decodemix(self,a,key):
		b=[x for x in a]
		pr=[]
		for x in range(len(b)):
			key=self.microrand(key)
			r1=key%(len(b)-x)+x
			pr.append(r1)
		for x in range(len(b)-1,-1,-1):
			b[x],b[pr[x]]=b[pr[x]],b[x]
		return ''.join(b)

	def getencode(self,s):
	    ans=''
	    k1=0
	    key1=self.microrand(self.key)
	    key2=self.microrand(-self.key)
	    s=self.encodemix(s,key2)
	    for x in s:
	        key1=self.microrand(key1)
	        ans+=chr((ord(x)+key1+k1)%(16**3))
	        k1=ord(x)
	    ans=self.encodemix(ans,self.microrand(-key2))
	    return ans

	def getdecode(self,s):
	    ans=''
	    k1=0
	    key1=self.microrand(self.key)
	    key2=self.microrand(-self.key)
	    s1=self.decodemix(s,self.microrand(-key2))
	    for x in s1:
	        key1=self.microrand(key1)
	        ans+=chr((ord(x)-key1-k1)%(16**3))
	        k1=ord(ans[0])
	    ans=self.decodemix(ans,key2)
	    return ans

class Tree:
    def __init__(self):
        self._graph=[[]]
        self._nums=[0]
        self._isword=[0]

    def addword(self,word,v=0):
        self._nums[v]+=1
        if len(word)>0:
            use=False
            for b,el in self._graph[v]:
                if b==word[0]:
                    self.addword(word[1:],el)
                    use=True
            if not use:
                self._graph.append([])
                self._graph[v].append((word[0],len(self._graph)-1))
                self._nums.append(0)
                self._isword.append(0)
                self.addword(word[1:],len(self._graph)-1)
        else:
            self._isword[v]+=1

    def removeword(self,word,v=0):
        if len(word)>0:
            use=False
            for b,el in self._graph[v]:
                if b==word[0]:
                    if self.removeword(word[1:],el):
                        use=True
            if use:
                self._nums[v]-=1
            return use
        else:
            if self._isword[v]>0:
                self._nums[v]-=1
                self._isword[v]-=1
                return True
            else:
                return False

    def numofword(self,word,v=0):
        if len(word)>0:
            use=False
            for b,el in self._graph[v]:
                if b==word[0]:
                    return self.numofword(word[1:],el)
                    use=True
            if not use:
                return 0
        else:
            return self._nums[v]

    def getisword(self,word,v=0):
        if len(word)>0:
            use=False
            for b,el in self._graph[v]:
                if b==word[0]:
                    return self.getisword(word[1:],el)
                    use=True
            if not use:
                return 0
        else:
            return self._isword[v]

    def getwords(self,word,v=0,newword=''):
        if len(word)>0:
            use=False
            for b,el in self._graph[v]:
                if b==word[0]:
                    return self.getwords(word[1:],el,newword+b)
                    use=True
            if not use:
                return []
        else:
            ans=[]
            for i in range(self._isword[v]):
                ans.append(newword)
            for b,el in self._graph[v]:
                ans+=self.getwords(word[1:],el,newword+b)
            return ans

    def merge(self,other,v=0,v2=0):
        self._nums[v]+=other._nums[v2]
        self._isword[v]+=other._isword[v2]
        a=dict()
        for letter,elem in self._graph[v]:
            a[letter]=elem
        for letter,elem in other._graph[v2]:
            if letter in a:
                self.merge(other,a[letter],elem)
                del a[letter]
            else:
                self._graph.append([])
                self._graph[v].append((letter,len(self._graph)-1))
                self._nums.append(0)
                self._isword.append(0)
                self.merge(other,len(self._graph)-1,elem)

    def index(self,word,v=0):
        if len(word)>0:
            use=0
            ans=0
            self._graph[v].sort()
            for b,el in self._graph[v]:
                if b==word[0]:
                    prans=self.index(word[1:],el)
                    if prans==None:
                        use=-1
                    else:
                        ans+=prans+self._isword[v]
                        use=1
                elif use==0:
                    ans+=self._nums[el]
            if use==1:
                return ans
            return None
        else:
            if self._isword[v]>0:
                return 0
            else:
                return None
    
    def rindex(self,word,v=0):
        if len(word)>0:
            use=0
            ans=0
            self._graph[v].sort()
            for b,el in self._graph[v]:
                if b==word[0]:
                    prans=self.rindex(word[1:],el)
                    if prans==None:
                        use=-1
                    else:
                        ans+=prans+self._isword[v]
                        use=1
                elif use==0:
                    ans+=self._nums[el]
            if use==1:
                return ans
            return None
        else:
            if self._isword[v]>0:
                return self._isword[v]-1
            else:
                return None

    def getofindex(self,ind,v=0,prans=-1,newword=''):
        if ind>=self._nums[0] or ind<0:
            return None
        ans=prans+self._isword[v]
        self._graph[v].sort()
        for b,el in self._graph[v]:
            if ans+self._nums[el]<ind:
                ans+=self._nums[el]
            else:
                answord=self.getofindex(ind,el,ans,newword+b)
                if answord!=False:
                    return answord
                else:
                    break
        if ind<=ans<ind+self._isword[v]:
            return newword
        else:
            return False

a=Tree()
a.addword('hello')
a.addword('hello')
a.addword('hell')
a.addword('hell')
a.addword('hellsas')
a.addword('hellsas')
a.addword('hells')
a.addword('qwj')
a.addword('jsodfj')
a.addword('rgjs')
a.addword('')
a.addword('')

b=a.getwords('')
b.sort()
for x in b:
    print(x==a.getofindex(a.index(x)),x==a.getofindex(a.rindex(x)))