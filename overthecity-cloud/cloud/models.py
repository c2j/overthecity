from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from datetime import datetime

class DetectWarning(models.Model):
    agent_id = models.CharField(_('Agent ID'),
                                  max_length=30,
                                  blank=True)
    detect_time = models.DateTimeField(default=datetime.now())
    coord_x = models.CharField(_('X location'),
                            max_length=20,
                            blank=True,
                            null=True)
    coord_y = models.CharField(_('Y location'),
                            max_length=20,
                            blank=True,
                            null=True)
    gps_att = models.CharField(_('Y location'),
                            max_length=20,
                            blank=True,
                            null=True)
    gps_long = models.CharField(_('Y location'),
                            max_length=20,
                            blank=True,
                            null=True)
