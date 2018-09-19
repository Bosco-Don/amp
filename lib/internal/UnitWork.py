# coding: utf-8
#!/usr/bin/python

#주요 Command
"""plaso, psort
	###################
	[log2timeline]
	>log2timeline.exe –z Asia/Seoul --workers 10 "F:\_.External\PFPCase_1469265662.34\Test\CaseData\C\plaso_output_4.dump" "F:\_.External\PFPCase_1469265662.34\Test\CaseData\C\Extract\Copy_1469266989.32\C"

	[psort, Sql4n6]
	>psort.exe -o Sql4n6 -w "F:\_.External\PFPCase_1469265662.34\Test\CaseData\C\plaso_output_4.db" --slicer "F:\_.External\PFPCase_1469265662.34\Test\CaseData\C\plaso_output_4.dump" "date > '2014-08-01' AND date < '2016-07-30'"

	[psort, csv]
	>psort.exe -o L2tcsv -w "F:\_.External\PFPCase_1469265662.34\Test\CaseData\C\plaso_output_4.csv" --slicer "F:\_.External\PFPCase_1469265662.34\Test\CaseData\C\plaso_output_4.dump" "date > '2014-08-01' AND date < '2016-07-30'"
"""

"""#마운트 테스트(MIP)
	[mount, MIP5]
	C:\Program Files (x86)\GetData\Mount Image Pro v5>MIP5.exe mount "Q:\Dropbox\0. [zurum]\4. [교안(책)] (바이블)\_. 실습 자료\[T] 3.10 Forensic Analysis Process\PC 이미지\Evidence_PC.001" /L:Z /B:F /A:T /T:1
	C:\Program Files (x86)\GetData\Mount Image Pro v5>MIP5.exe mount "Q:\Dropbox\0. [zurum]\4. [교안(책)] (바이블)\_. 실습 자료\[T] 3.10 Forensic Analysis Process\PC 이미지\e01_ver\Evidence_PC.E01" /L:Z /B:F /A:T /T:1
	Mount Image Pro. v5.0.6 (1068)
	Mounting in progress, wait...

	Image "Q:\Dropbox\0. [zurum]\4. [교안(책)] (바이블)\_. 실습 자료\[T] 3.10 Forensic Analysis Process\PC 이미지\Evidence_PC.001" contains 1 partition(s).

	Access Mode: Block Mode
	-----------------------------------
	PhysDrive    Not bootable
	  Capacity is:  30.00 GB
	  Drive Letter: PHYSICALDRIVE10
	  Is HardDisk:  True
	  Is Optical:   False
	  Label is:
	  Type is:      Physical
	-----------------------------------
	Partition 1:    Active / Bootable
	  Capacity is:  29.99 GB
	  Drive Letter: Z:
	  Is HardDisk:  True
	  Is Optical:   False
	  Label is:
	  Type is:      NTFS/OS2 HPFS

	Q:\Dropbox\0. (PFP)\PFP Source>".\PFPModule\PFPLib\InternalModules\Mount Image Pro v5\MIP5.exe" unmount /all
	Mount Image Pro. v5.0.6 (1068)
	Closing all mounted images...
	The image(s) is closed.
"""

"""#마운트 테스트 (OSF) <-- 얘는 이미지 경로에 대괄호 있으면 진행 안됨..
	>".\PFPModule\PFPLib\InternalModules\OSFMount(x86)\OSFMount.com" -a -t file -f "E:\img\overwork_2\E01\150629.E01" -m #:	<---#을 하면 알아서 drvletter 찾는다. 
	C:\Program Files\OSFMount>osfmount -a -t file -f "Q:\Dropbox\0. [zurum]\4. [교안(책)] (바이블)\_. 실습 자료\[T] 3.10 Forensic Analysis Process\PC 이미지\Evidence_PC.001" -m z:
	C:\Program Files\OSFMount>osfmount -a -t file -f "D:\e01_ver\Evidence_PC.E01" -m z:

	C:\Program Files\OSFMount>osfmount -a -t file -f "D:\e01_ver\Evidence_PC.E01" -m z:
	Creating device...
	Created device 0: z: -> D:\e01_ver\Evidence_PC.E01
	Notifying applications...
	Done.

	C:\Program Files\OSFMount>osfmount -l -m z:
	Mount point: z:
	Image file: \??\D:\e01_ver\Evidence_PC.E01
	Image file offset: 32256 bytes
	Size: 32201938944 bytes (29.99 GB), ReadOnly, File Type Virtual Disk, HDD.

	>".\PFPModule\PFPLib\InternalModules\OSFMount(x86)\OSFMount.com" -D -m z:
	C:\Program Files\OSFMount>osfmount -d -m z:
	C:\Program Files\OSFMount>osfmount -D -m z:	<---요거는 강제 dismount
	Flushing file buffers...
	Locking volume...
	Dismounting filesystem...
	Removing device...
	Removing mountpoint...
	Done.
"""

"""Python image mounter (https://pypi.python.org/pypi/imagemounter/2.0.4)
	https://pypi.python.org/pypi/imagemounter/2.0.4
	https://github.com/ralphje/imagemounter <--- 요게 본 사이트
"""


import os
import platform
print platform.architecture()
print os.environ
print os.path.isdir("g:")

"""
import os

import sys
reload(sys)
sys.setdefaultencoding('cp949')

print "Hello World"
"""

"""
#폴더 순회, 

#데이터 접근
#---URL 접근(htm, 파일 다운)
#---파일 경로 처리
os.path.split(Path)
os.path.join(Dir, FileName)
#---파일 접근
fp = open(Path, 'r') #Text 모드(읽기모드)
fp = open(Path, 'rb') #Binary 모드(읽기모드)
fp = open(Path, 'w') #Text 모드(쓰기모드)
fp = open(Path, 'a') #Text 모드(추가모드)
fp.close()
#---Hex 데이터 표현
'\x4b\x44\x54\x5f\x50\x4c\x43\x5f\x4d\x00\x52\x00\x00\x0a\x4d\x30\x30\x30\x32\x30\x30\x30\x00\x32\x04\xfa'

#파일 처리
"""

"""#---전체 순차 읽기
	for root, dirs, files in os.walk(self.CasePath):
		for file in files:
			if os.path.split(file)[0] not in (self.CasePath + "\\"):
"""


"""
#---특정 부분 읽기
#---En/Decoding, 암/복호화, 압축/해제
#---for 문
for element in list:
for idx in range(1,5):
for idx in range(10,1,-1):
#---문자열 처리
#정규표현식

#DB 접근/처리
"""

"""#Netword 처리
    import socket
	
    ip = "10.16.12.138"
    port = 10061
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(8)
    try :
        sock.connect((ip, port))

    except socket.error as e :
        print "Socket error : " + str(e)
        return 
    
    sock.send('\x4b\x44\x54\x5f\x50\x4c\x43\x5f\x4d\x00\x52\x00\x00\x0a\x4d\x30\x30\x30\x32\x30\x30\x30\x00\x32\x04\xfa')
    reply = sock.recv(1024)

    print str(reply)
"""