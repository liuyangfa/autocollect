# -*- coding: utf-8 -*-

import sys

from django.forms import ModelForm, forms

from models import Physical

reload(sys)
sys.setdefaultencoding("utf-8")



class PhysicalForm(ModelForm):
    # 服务器类型为vmware时，必须填写其所属的vcenter服务器
    def clean_vcenterid(self):
        data = self.cleaned_data['vcenterid']
        type = self.cleaned_data['type']
        if type == '2':
            if not data:
                raise forms.ValidationError('vcenter must be selected')
            return data

    class Meta:
        model = Physical
        fields = '__all__'
