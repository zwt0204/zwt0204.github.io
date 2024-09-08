<<<<<<< HEAD
---
layout:     post
title:      "lightgbm"
subtitle:   " \"lightgbm\""
date:       2022-08-15 18:00:00
mathjax: true
author:     "zwt"
header-img: "img/post-bg-2015.jpg"
catalog: false
tags:
    - spark
---
* TOC
{:toc}
# 配置
```
config('spark.jars.packages', "com.microsoft.ml.spark:mmlspark_2.11:0.18.1")
.config('spark.jars', "./notebook/jar/lightgbmlib-2.2.350.jar")
```
#  使用
```
from mmlspark.lightgbm import LightGBMClassifier
lgb = LightGBMClassifier(
    objective="binary",
    boostingType='gbdt',
    isUnbalance=True,
    featuresCol='features',
    labelCol='label',
    maxBin=60,
    baggingFreq=1,
    baggingSeed=696,
    earlyStoppingRound=30,
    learningRate=0.1,
    lambdaL1=1.0,
    lambdaL2=45.0,
    maxDepth=3,
    numLeaves=128,
    baggingFraction=0.7,
    featureFraction=0.7,
    # minSumHessianInLeaf=1,
    numIterations=100,
    verbosity=50
)
=======
---
layout:     post
title:      "lightgbm"
subtitle:   " \"lightgbm\""
date:       2022-08-15 18:00:00
mathjax: true
author:     "zwt"
header-img: "img/post-bg-2015.jpg"
catalog: false
tags:
    - spark
---
* TOC
{:toc}
# 配置
```
config('spark.jars.packages', "com.microsoft.ml.spark:mmlspark_2.11:0.18.1")
.config('spark.jars', "./notebook/jar/lightgbmlib-2.2.350.jar")
```
#  使用
```
from mmlspark.lightgbm import LightGBMClassifier
lgb = LightGBMClassifier(
    objective="binary",
    boostingType='gbdt',
    isUnbalance=True,
    featuresCol='features',
    labelCol='label',
    maxBin=60,
    baggingFreq=1,
    baggingSeed=696,
    earlyStoppingRound=30,
    learningRate=0.1,
    lambdaL1=1.0,
    lambdaL2=45.0,
    maxDepth=3,
    numLeaves=128,
    baggingFraction=0.7,
    featureFraction=0.7,
    # minSumHessianInLeaf=1,
    numIterations=100,
    verbosity=50
)
>>>>>>> d5005ecd9eaf3ce32260dc1b7d831c7f2a1a85f3
```