# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=64, verbose_name="产品")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "产品"
        verbose_name_plural = "产品"

class UserProfile(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="产品")
    env_list = (
        ('prod', 'prod'),
        ('qa', 'qa'),
        ('dev', 'dev')
    )
    env = models.CharField(choices=env_list, max_length=4, verbose_name='环境')
    mysql_host = models.CharField(max_length=128, verbose_name='MySQL地址')
    mysql_port = models.IntegerField(verbose_name='MySQL端口')
    mysql_user = models.CharField(max_length=20, verbose_name='MySQL用户')
    mysql_pwd = models.CharField(max_length=64, verbose_name='MySQL密码')

    def __str__(self):
        return "%s-%s" % (self.product, self.env)

    class Meta:
        unique_together = ('product', 'env')
        verbose_name_plural = "账号信息"
        verbose_name = "账号信息"

class SecretDB(models.Model):
    name = models.CharField(max_length=64, verbose_name="库名")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "私密库"
        verbose_name_plural = "私密库"


