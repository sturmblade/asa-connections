#! /usr/bin/env python

import sys, operator
from collections import Counter


def Connections(filename):

  #Generating a temporary file that contains the user list

  in_file = open(filename, 'r')
  temp_file = in_file.readlines()
  temp_file.sort()
  in_file.close()

  out_file_UDP = open('UDP_counters_'+filename, 'w')
  out_file_TCP = open('TCP_counters_'+filename, 'w')
  out_file_IP = open('IP_counters_'+filename, 'w')
  out_file_Traffic = open('IP_conversations_'+filename, 'w')
  
  all_TCP_entries = []
  all_UDP_entries = []
  all_IP_addresses = []
  an_entry = []
  all_entries_with_traffic = {}

  for lines in temp_file:
    fields = lines.split(' ')
    if fields[0] == 'TCP':
      # Creating a list of all TCP connections 	
      first_ip = fields[3].split(':')[0]
      second_ip = fields[6].split(':')[0]
      first_interface = fields[1]
      second_interface = fields[4]
      conn_bytes = int(fields[10].strip(','))


      # Extracting the full TCP connection entry and adding to the list
      a_TCP_entry = [first_interface+' '+first_ip+' '+second_interface+' '+second_ip]
      all_TCP_entries.append(a_TCP_entry)

      # Keeping track of the total number of bytes per connection 
      a_traffic_entry = "'"+''.join(a_TCP_entry)+"'"

      if a_traffic_entry in all_entries_with_traffic.keys():
        all_entries_with_traffic[a_traffic_entry] += conn_bytes
      else:
        all_entries_with_traffic[a_traffic_entry] = conn_bytes
      
      first_ip = [first_ip]
      second_ip = [second_ip]
      all_IP_addresses.append(first_ip)
      all_IP_addresses.append(second_ip) 

    elif fields[0] == 'UDP': 
      # Creating a list of all UDP connections 
      first_ip = fields[3].split(':')[0]
      second_ip = fields[6].split(':')[0]
      first_interface = fields[1]
      second_interface = fields[4]
      conn_bytes = int(fields[10].strip(','))

      # Extracting the full UDP connection entry and adding to the list
      a_UDP_entry = [first_interface+' '+first_ip+' '+second_interface+' '+second_ip]
      all_UDP_entries.append(a_UDP_entry) 

      # Keeping track of the total number of bytes per connection 
      a_traffic_entry = "'"+''.join(a_UDP_entry)+"'"

      if a_traffic_entry in all_entries_with_traffic.keys():
        all_entries_with_traffic[a_traffic_entry] += conn_bytes
      else:
        all_entries_with_traffic[a_traffic_entry] = conn_bytes      

      first_ip = [first_ip]
      second_ip = [second_ip]
      all_IP_addresses.append(first_ip)
      all_IP_addresses.append(second_ip)      


  # Counting the number of occurence per TCP entry
  TCP_counters = Counter(sum(all_TCP_entries, []))

  # Counting the number of occurence per UDP entry
  UDP_counters = Counter(sum(all_UDP_entries, []))

  # Counting the number of occurence per IP address
  #print all_IP_addresses
  IP_counters = Counter(sum(all_IP_addresses, [])) 

  # Getting the top 10 TCP for example   
  top_TCP_list = TCP_counters.most_common(10) 
  print '='*70+'\n'
  print "Top 10 TCP connections:"
  for each_entry in top_TCP_list:
    print ("{0:60}{1:10}".format(each_entry[0],each_entry[1]))

  # Getting the top 10 UDP for example  
  top_UDP_list = UDP_counters.most_common(10) 
  print '='*70+'\n'
  print "Top 10 UDP connections:" 
  for each_entry in top_UDP_list:
    print ("{0:60}{1:10}".format(each_entry[0],each_entry[1]))

  # Getting the top 10 IP addresses for example 
  top_IP_list = IP_counters.most_common(10) 
  print '='*70+'\n'
  print "Top 10 connections per IP address:" 

  for each_entry in top_IP_list:
    print ("{0:60}{1:10}".format(each_entry[0],each_entry[1]))        
  
  # Sorting the lists 
  TCP_counters_list = TCP_counters.items()
  TCP_counters_ordered_list = sorted(TCP_counters_list, key=lambda tup: tup[1], reverse = True)
  
  UDP_counters_list = UDP_counters.items()
  UDP_counters_ordered_list = sorted(UDP_counters_list, key=lambda tup: tup[1], reverse = True)

  IP_counters_list = IP_counters.items()
  IP_counters_ordered_list = sorted(IP_counters_list, key=lambda tup: tup[1], reverse = True)
 
  # Getting the top 25 conversations for example
  # Sorting the traffic dictionary and keeping the top 25
  sorted_traffic_top = sorted(all_entries_with_traffic.items(), key=operator.itemgetter(1), reverse = True)[:25]
  
  print '='*80+'\n'
  print "Top 25 conversations:"   

  for each_entry in sorted_traffic_top:
    print ("{0:70}{1:10}".format(each_entry[0].strip("'"),each_entry[1]))        


  # Saving the result in file 
  for each_entry in TCP_counters_ordered_list:
    out_file_TCP.write(each_entry[0]+': '+str(each_entry[1])+'\n')
  for each_entry in UDP_counters_ordered_list:
    out_file_UDP.write(each_entry[0]+': '+str(each_entry[1])+'\n')
  for each_entry in IP_counters_ordered_list:
    out_file_IP.write(each_entry[0]+': '+str(each_entry[1])+'\n') 

  sorted_traffic = sorted(all_entries_with_traffic.items(), key=operator.itemgetter(1), reverse = True)
  for each_entry in sorted_traffic:
    out_file_Traffic.write(each_entry[0]+': '+str(each_entry[1])+'\n')     

  print '='*80+'\n'
  print ("{0:35}{1:15}".format("Total number of connections: ",len(temp_file)))
  print '='*50+'\n'
  print ("{0:35}{1:15}".format("Total number of TCP connections: ",len(all_TCP_entries)))
  print ("{0:35}{1:15}".format("Unique TCP conversations: ",len(TCP_counters)))
  print '='*50+'\n'
  print ("{0:35}{1:15}".format("Total number of UDP connections: ",len(all_UDP_entries)))
  print ("{0:35}{1:15}".format("Unique UDP conversations: ",len(UDP_counters)))
  print '='*50+'\n'
  print ("{0:35}{1:15}".format("Total number of IP addresses: ",len(IP_counters_list)))


  out_file_UDP.close()  
  out_file_TCP.close()
  out_file_IP.close()
  out_file_Traffic.close()
 

def main():
    # Script to extract top talkers  
  args = sys.argv[1:]
  if (len(args) != 1):
    print 'usage: python ASA_sort_connections.py filename'
    sys.exit(1)
  
  filename = args[0]
  
  Connections(filename)
  
  print '='*80+'\n'
  print 'Check the results in the following file: UDP_counters_'+filename 
  print 'Check the results in the following file: TCP_counters_'+filename 
  print 'Check the results in the following file: IP_counters_'+filename
  print 'Check the results in the following file: IP_conversations_'+filename
 


if __name__ == "__main__":
  main()
