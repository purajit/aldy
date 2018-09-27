#!/usr/bin/env python
# 786

# Aldy source: test_cn.py
#   This file is subject to the terms and conditions defined in
#   file 'LICENSE', which is part of this source code package.

from nose.tools import *

import aldy.cn
from aldy.gene import Gene
from aldy.common import *


def assert_cn_model(expected, cov):
   cyp2d6 = Gene(script_path('aldy.resources.genes', 'cyp2d6.yml'))
   sols = aldy.cn.solve_cn_model(cyp2d6, 
                         cn_configs=cyp2d6.cn_configs, 
                         max_cn=20, 
                         region_coverage=cov, 
                         solver='gurobi')
   assert_equal(len(sols), len(expected))
   sols = sorted([sorted(s.solution.items()) for s in sols])
   expected = sorted([sorted(s.items()) for s in expected])
   assert_equal(sols, expected)
   
def test_many_copies_multiple_solutions():
   # HG00465
   assert_cn_model(
      [{'1': 2, '36': 2},
       {'1': 2, '61': 2},
       {'1': 2, '63': 2}],
      {GeneRegion(1, 'e'): (3.849646861540177, 2.1395460667257846), 
       GeneRegion(1, 'i'): (3.338316245135396, 2.5479677252055217), 
       GeneRegion(2, 'e'): (3.7298798768474346, 2.142931947310467), 
       GeneRegion(2, 'i'): (4.052118869192745, 1.9735716019274423), 
       GeneRegion(3, 'e'): (4.54735023055686, 1.87488611011621), 
       GeneRegion(5, 'e'): (3.9511309438084194, 2.0961636580560294), 
       GeneRegion(5, 'i'): (4.137338585699026, 2.0973819541039425), 
       GeneRegion(6, 'e'): (4.0175572874738705, 2.049507076017088), 
       GeneRegion(6, 'i'): (3.990280521226456, 1.8785516831838405), 
       GeneRegion(9, 'e'): (2.5436703140578256, 3.6071603617051724), 
       GeneRegion(1, 'pce'): (0, 4.1413471334142375)})

def test_right_fusion():
   # HG01190
   assert_cn_model(
      [{'1': 1, '68': 1}],
      {GeneRegion(1, 'e'): (1.8930745191720157, 2.084669650842661), 
       GeneRegion(1, 'i'): (1.9497254755644196, 2.0202584206726923), 
       GeneRegion(2, 'e'): (0.9163238883731375, 2.852674345883635), 
       GeneRegion(2, 'i'): (1.060490056361081, 3.067216873759015), 
       GeneRegion(3, 'e'): (1.184419152569399, 2.7596248366837686), 
       GeneRegion(5, 'e'): (1.0381335955641755, 3.3204358070262163), 
       GeneRegion(5, 'i'): (1.1508467055098155, 3.2331971543959837), 
       GeneRegion(6, 'e'): (1.066256525480151, 3.1833405997884725), 
       GeneRegion(6, 'i'): (1.1335552155849216, 2.953136109086207), 
       GeneRegion(9, 'e'): (1.310423297300959, 2.722438452401353), 
       GeneRegion(1, 'pce'): (0, 3.1630048011763616)})

def test_normal():
   # HG02260
   assert_cn_model(
      [{'1': 2}],
      {GeneRegion(1, 'e'): (1.8404691764265304, 2.0857910075016175), 
       GeneRegion(1, 'i'): (1.903113836789805, 2.0085212340180862), 
       GeneRegion(2, 'e'): (2.043975104515077, 1.9288167855888463), 
       GeneRegion(2, 'i'): (1.9131964445631862, 1.8656695352960695), 
       GeneRegion(3, 'e'): (2.0366694974274973, 1.8861463557999658), 
       GeneRegion(5, 'e'): (1.8515736715903186, 2.1882438972864158), 
       GeneRegion(5, 'i'): (1.9531022017590338, 2.044349862608799), 
       GeneRegion(6, 'e'): (2.092317166317333, 2.1187410721896787), 
       GeneRegion(6, 'i'): (2.0568727879055015, 1.9060136594971473), 
       GeneRegion(9, 'e'): (2.1798377730315583, 1.895663436746719), 
       GeneRegion(1, 'pce'): (0, 2.0132890977658606)})

def test_deletion():
   # NA12336
   assert_cn_model(
      [{'1': 1, '5': 1}],
      {GeneRegion(1, 'e'): (1.0308827464338521, 1.9988980953893645), 
       GeneRegion(1, 'i'): (1.3748167540606304, 1.6491147374469535), 
       GeneRegion(2, 'e'): (0.9924878173891469, 1.6342665445332492), 
       GeneRegion(2, 'i'): (1.0290405661572466, 1.9198712562073412), 
       GeneRegion(3, 'e'): (1.167022126990559, 1.7540850916838109), 
       GeneRegion(5, 'e'): (0.9421579094291783, 2.210820632011098), 
       GeneRegion(5, 'i'): (0.9298106372896381, 2.052920209456965), 
       GeneRegion(6, 'e'): (0.9427811132907081, 1.969435816986854), 
       GeneRegion(6, 'i'): (0.9973218427542927, 1.885548111595809), 
       GeneRegion(9, 'e'): (1.0982056490431031, 1.846590922907834), 
       GeneRegion(1, 'pce'): (0, 1.9869362954454903)})

def test_right_fusion_with_copy():
   # NA12878
   assert_cn_model(
      [{'1': 2, '68': 1}],
      {GeneRegion(1, 'e'): (2.6537221395440223, 2.001557876770771), 
       GeneRegion(1, 'i'): (2.425858398883405, 2.3148672916870043), 
       GeneRegion(2, 'e'): (1.8623061177538052, 2.9641961390512446), 
       GeneRegion(2, 'i'): (2.0050476187827884, 2.9440140210172157), 
       GeneRegion(3, 'e'): (2.237543359619445, 2.572100071780838), 
       GeneRegion(5, 'e'): (1.9376600216945707, 3.084516358486409), 
       GeneRegion(5, 'i'): (1.9339774367820306, 3.0267463128264147), 
       GeneRegion(6, 'e'): (1.8525080453423006, 2.9231659656677027), 
       GeneRegion(6, 'i'): (1.9799757975037504, 2.9167383850087094), 
       GeneRegion(9, 'e'): (2.1669406413105645, 2.640311897155015), 
       GeneRegion(1, 'pce'): (0, 3.038743530465482)})

def test_normal2():
   # NA19239
   assert_cn_model(
      [{'1': 2}],
      {GeneRegion(1, 'e'): (1.6961734008406737, 2.2349929110372178), 
       GeneRegion(1, 'i'): (2.0603204283429464, 2.018605131495889), 
       GeneRegion(2, 'e'): (2.0000283790837172, 1.922007756022532), 
       GeneRegion(2, 'i'): (2.0129798962890475, 2.149008726605769), 
       GeneRegion(3, 'e'): (2.174850450379796, 1.9104991568002714), 
       GeneRegion(5, 'e'): (1.9325813912205059, 2.2576772957088433), 
       GeneRegion(5, 'i'): (2.0313761220117654, 2.065837024862324), 
       GeneRegion(6, 'e'): (1.9981320676660355, 2.0114711486863524), 
       GeneRegion(6, 'i'): (1.9534568439799365, 2.014615928506664), 
       GeneRegion(9, 'e'): (2.112206546899065, 2.03780525113827), 
       GeneRegion(1, 'pce'): (0, 2.1584560384332665)})

def test_left_fusion():
   # NA19790
   assert_cn_model(
      [{'1': 2, '78': 1}],
      {GeneRegion(1, 'e'): (1.9410696110645995, 2.0690064969758803), 
       GeneRegion(1, 'i'): (2.016614473557294, 1.9104154500394386), 
       GeneRegion(2, 'e'): (2.0613031644631463, 2.035897649513522), 
       GeneRegion(2, 'i'): (2.0889261937857615, 2.0979858766205375), 
       GeneRegion(3, 'e'): (2.1226604528653352, 1.9755999450939397), 
       GeneRegion(5, 'e'): (2.8184771375478994, 1.2211864391478575), 
       GeneRegion(5, 'i'): (2.943847395475305, 1.0068219719063978), 
       GeneRegion(6, 'e'): (2.7618724953751372, 0.9867524063314977), 
       GeneRegion(6, 'i'): (2.8389886375449014, 0.9691568703785511), 
       GeneRegion(9, 'e'): (3.1541146103253315, 1.0116708525386684), 
       GeneRegion(1, 'pce'): (0, 1.0484819551044866)})
