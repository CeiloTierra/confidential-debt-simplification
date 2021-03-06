from django.db import models
import uuid

key_length = 400;

class Group(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    name = models.CharField(max_length=80)

    key = models.CharField(max_length=key_length)
    
    def __str__(self):
        return self.name

class User(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    key = models.CharField(primary_key=True, max_length=key_length)
    email = models.EmailField(max_length=254)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.key
        

class Invitation(models.Model):
	
	inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inviter')
	invitee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitee')
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	signature_inviter = models.CharField(max_length=key_length)
	signature_group = models.CharField(max_length=key_length, default='')
	signature_invitee = models.CharField(max_length=key_length, default='')
	secret_code = models.CharField(max_length=20) 
	
	def __str__(self):
		return str(self.uuid)

	
	



