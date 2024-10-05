terraform {
  required_providers {
    oci = {
      source = "oracle/oci"
    }
  }
}

provider "oci" {
  region              = "us-sanjose-1"
  auth                = "SecurityToken"
  config_file_profile = "learn-terraform"
}

resource "oci_core_vcn" "internal" {
  dns_label      = "internal"
  cidr_block     = "172.16.0.0/20"
  compartment_id = "<your_compartment_OCID_here>"
  display_name   = "My internal VCN"
}



resource "oci_core_security_list" "ingress_tcp" {
    compartment_id = "<your_compartment_OCID_here>"
    display_name   = "Ingress TCP Security List"

    ingress_security_rules {
        protocol = "6"  # TCP
        source   = "0.0.0.0/0"  # Allow traffic from any source
        tcp_options {
            destination_port_range {
                min = 80
                max = 8080
            }
        }
    }
}

resource "oci_core_instance" "example" {
    # ... other instance configuration ...

    vnic {
        # ... other VNIC configuration ...

        security_list_ids = [oci_core_security_list.ingress_tcp.id]
    }
}