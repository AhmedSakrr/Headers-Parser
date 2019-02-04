# Headers-Parser
WhatIsMyBrowser browser headers parser

# Required
`pip install requests bs4`

# About
```python
AgentParser(
  browser,  # String. Sort by browser. Values: chrome, opera, firefox
  pages,  # Int. Pages where we search.
  full,  # Bool. Receive full user agent string or by: devices and versions
  min_ver,  # Int. Minimun browser version for parse. I recomend left by default
  os,  # String. Sort by OS. Values: Windows, Linux, Android, MacOS, iOS or Any
  platform  # String. Sort by platform. Values: Mobile, Computer or Any
)
```  
If you use param `full` as `True` see `Example 1` or see `Example 2`

# Example Usage
## Example 1
```python
import agentparser

agent = AgentParser('chrome')
print(agent.ua_list)
```  
Output:  
```['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/5... and more others```

## Example 2
```python
import agentparser

agent = AgentParser('chrome', pages=2, full=False, os='Android')
print(agent.devices)
print(agent.versions)
```  
Output:  
```
['Linux; Android 6.0.1; SM-J700M', 'Linux; Android 8.1.0; Moto G (5)'... and more others]
['70.0.3538.80', '69.0.3497.100', '68.0.3440.91']
```
