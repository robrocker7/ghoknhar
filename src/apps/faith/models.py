from django.db import models

# Create your models here.
class Vote(models.Model):
    like = models.BooleanField(default=False)
    ip_address = models.IPAddressField()
    date_created = models.DateTimeField(auto_now_add=True)

class Bar(models.Model):
    votes = models.ManyToManyField(Vote)
    date_created = models.DateTimeField(auto_now_add=True)

    def has_voted(self, ip):
        return self.check_duplicate_ip(ip)

    def check_duplicate_ip(self, ip):
        votes = self.vote_set.filter(ip_address=ip)
        if votes > 0:
            return True
        return False
    
    def has_faith(self, ip):
        if not self.check_duplicate_ip(ip):
            vote = Vote()
            vote.like = True
            vote.ip_address = ip
            vote.save()
            self.votes.add(vote)

    def no_faith(self, ip):
        if not self.check_duplicate_ip(ip):
            vote = Vote()
            vote.like = False
            vote.ip_address = ip
            vote.save()
            self.votes.add(vote)

    def faith_count(self):
        return self.vote_set.filter(like=True).count()

    def no_faith_count(self):
        return self.vote_set.filter(like=False).count()
