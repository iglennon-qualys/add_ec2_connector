THIS SCRIPT IS PROVIDED TO YOU "AS IS." TO THE EXTENT PERMITTED BY LAW, QUALYS HEREBY DISCLAIMS ALL WARRANTIES AND LIABILITY FOR THE PROVISION OR USE OF THIS SCRIPT. IN NO EVENT SHALL THESE SCRIPTS BE DEEMED TO BE CLOUD SERVICES AS PROVIDED BY QUALYS

# EC2_Connectors_Final.py
Processes a CSV input to add AWS EC2 Connectors to a Qualys subscription
Console output as well as debug_file.txt will have both success & failure logs.

# AWS_EC2_CONNECTOR_INFO.csv

Info : csv files contains below attributes required for AWS connector
Script looks for AWS_CONNECTOR_INFO.csv in the directory the script runs from

> ARN,NAME,EXTID,REGION,MODULE

*EXTID must be an INT from 9-90 in length* Example: 98765456787654567821

*REGION must be single spaced list of regions or "ALL"*


*Examples*
> ALL

> us-east-1

> us-east-1 us-west-1 us-west-2


*MODULES must be an list of modules to activate for connector*

*Examples:*
> VM

> "VM PC"

> "VM PC SCA"

# Script Usage
```text
EC2_Connectors_Final.py [-h] [-c] [-d] username api_endpoint

positional arguments:
  username         Qualys Username
  api_endpoint     Qualys API FQDN (e.g. qualysapi.qualys.com

optional arguments:
  -h, --help       show this help message and exit
  -c, --cloudview  Also add Cloud View connector with the same details
  -d, --debug      Enable debug output to file
```


# Script Requirements
This script is written in Python 3.7.4
This script requires the following PIP modules to run
Modules: sys, requests, datetime, os, time, csv, base64\

# Debug
Debug file for script run, located in ./debug folder with time/date stamp per line. To disable debug, comment out all lines containing "debug"


# License
Disclaimer: This script is provided as is, as an example. USE AT YOUR OWN RISK. NOT A SUPPORTED SOLUTION
# Copyright (c) 2020, Qualys All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met: * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer. * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution. * Neither the name of the Qualys nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL QUALYS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED ANDON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
