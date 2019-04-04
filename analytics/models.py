from django.db import models
from django.contrib.postgres.fields import ArrayField,JSONField
# Create your models here.
import datetime


class Match_Detail(models.Model):
    match_id = models.BigIntegerField(primary_key=True)
    match_data = JSONField()

class Account(models.Model):
    account_id = models.CharField(primary_key=True,max_length=64)
    name = models.CharField(max_length=25)
    solo_match_list = ArrayField(models.BigIntegerField(),default=list)
    flex_match_list = ArrayField(models.BigIntegerField(),default=list)
    refresh = models.DateTimeField('last refreshed for this account and queue',default=datetime.date.fromtimestamp(0))

class Champion(models.Model):
    champ_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=25)
    champ_data = JSONField()

class Aggregate_Account(models.Model):
    account_id = models.ForeignKey(Account,on_delete=models.CASCADE)
    solo_champion_stats = JSONField()
    flex_champion_stats = JSONField()
    total_champion_stats = JSONField()
