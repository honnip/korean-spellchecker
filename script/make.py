#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys
import subprocess

def usage():
	print("./script/make.py 새버전")
	print("예) ./script/make.py 0.7.1")
	
	print("Changelog 는 수동 변경 필요")
	sys.exit()




def get_old_ver():
	cmd = "grep initInstall /data/projects/korean-spellchecker/Firefox/install.js | awk -F',' '{print $3}' | grep -oP '\"\K[^\"\\047]+(?=[\"047])'"
	popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	cmd_result = popen.communicate()
	return cmd_result[0].decode("utf-8").replace("\n","")
	


if __name__ == "__main__":
	#아규먼트 수가 1이면 사용법 출력하고 종료
	if len(sys.argv) == 1 :
		usage()
	
	#필요 상수 지정
	old_ver = get_old_ver().replace("-1","")
	print("previous version: %s" % old_ver)
	
	new_ver = sys.argv[1]
	print("new version: %s" % new_ver)
	
	path = os.path.dirname(os.path.abspath(__file__)) + '/..'


	#사전 파일 다운로드
	cmd  = 'cd %s;' % path
	if int(new_ver.replace('.', '')) < 71: 
		dict_filename = 'ko-aff-dic-%s-for-hunspell-1.2.8' % new_ver
		cmd += 'wget -P dictionary https://github.com/spellcheck-ko/hunspell-dict-ko/releases/download/%s/%s.zip;' % (new_ver, dict_filename)
		cmd += 'unzip -d dictionary dictionary/ko-aff-dic-%s-for-hunspell-1.2.8;' % (new_ver)
	else: #0.7.1 버전 이후부터 hunspell 1.2.8 버전을 따로 제공하지 않음
		dict_filename = 'ko-aff-dic-%s' % new_ver
		cmd += 'wget -P dictionary https://github.com/spellcheck-ko/hunspell-dict-ko/releases/download/%s/%s.zip;' % (new_ver, dict_filename)
		cmd += 'unzip -d dictionary dictionary/ko-aff-dic-%s;' % (new_ver)
	print(cmd.replace(";","\n"))
	os.system(cmd)
	
	#리브레오피스 확장 만들기
	cmd  = '\\cp -f dictionary/%s/LICENSE* LibreOffice;' % dict_filename
	cmd += '\\cp -f dictionary/%s/ko.aff LibreOffice/dictionaries/ko-KR.aff;' % dict_filename
	cmd += '\\cp -f dictionary/%s/ko.dic LibreOffice/dictionaries/ko-KR.dic;' % dict_filename
	cmd += "sed -i 's/%s-1/%s-1/g' LibreOffice/description.xml;" % (old_ver, new_ver)
	print(cmd.replace(";","\n"))
	os.system(cmd)
	
	
	#파이어폭스 확장 만들기
	cmd  = '\\cp -f dictionary/%s/LICENSE* Firefox;' % dict_filename
	cmd += '\\cp -f dictionary/%s/ko.aff Firefox/dictionaries/ko-KR.aff;' % dict_filename
	cmd += '\\cp -f dictionary/%s/ko.dic Firefox/dictionaries/ko-KR.dic;' % dict_filename
	cmd += "sed -i 's/%s-1/%s-1/g' Firefox/install.js;" % (old_ver, new_ver)
	cmd += "sed -i 's/%s-1/%s-1/g' Firefox/install.rdf;" % (old_ver, new_ver)
	print(cmd.replace(";","\n"))
	os.system(cmd)
	
	
	#zip 으로 묶기
	cmd  = 'cd Firefox;'
	cmd += 'zip -r ../bin/Korean_spell-checker-%s-1_FF.xpi ./*;' % new_ver
	cmd += 'cd ..;'
	cmd += 'cd LibreOffice;'
	cmd += 'zip -r ../bin/Korean_spell-checker-%s-1_LibO.oxt ./*;' % new_ver
	cmd += 'cd ..'
	print(cmd.replace(";","\n"))
	os.system(cmd)


	#불필요한 디렉토리 삭제
	cmd = 'rm -rf dictionary/%s' % dict_filename
	print(cmd.replace(";","\n"))
	os.system(cmd)


