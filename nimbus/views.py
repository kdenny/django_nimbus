# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import HttpResponse
from gspread_query import get_json_array

import os
from pprint import pprint

# Ensure that sheets are shared with nimbus-charts@nimbus-charts.iam.gserviceaccount.com
class GoogleSheetDataView(APIView):

    def get(self, request, sheet_id='0', sheet_name='none'):
        if (sheet_id != '0' and sheet_name != 'none'):
            sheet_url = 'https://docs.google.com/spreadsheets/d/' + sheet_id
            data = get_json_array(sheet_url, sheet_name)

        return Response(data)

