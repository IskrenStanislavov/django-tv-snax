from django.db import models

class AdminFiles(models.Model):
	# id, table, relationId, filePath, originalFileName, fieldName
    id          		= models.AutoField(primary_key=True)
    table    			= models.CharField(max_length=255)
    relationId 			= models.PositiveIntegerField()
    filePath       		= models.CharField(max_length=255)
    originalFileName  	= models.CharField(max_length=255)
    fieldName    		= models.CharField(max_length=255)

    class Meta:
        db_table = "_files"
        ordering = ("table", 'fieldName', 'relationId')
        unique_together = ("table", 'fieldName', 'relationId')

class AdminUsers(models.Model):
	# id, userName, password
    id           		= models.AutoField(primary_key=True)
    userName     		= models.CharField(max_length=255)
    password     		= models.CharField(max_length=255)
    is_superuser 		= is_staff = True

    class Meta:
        db_table = "_users"
