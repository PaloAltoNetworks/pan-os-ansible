## 1.0.0 (2023-10-06)


### Features

* **event_driven_ansible:** New plugin for event-driven ansible ([c4b627d](https://github.com/jamesholland-uk/pan-os-ansible/commit/c4b627dac496f7233ca6016aa85f60c8378ada41))
* **panos_address_group:** Add `gathered_filter` ([6a3b230](https://github.com/jamesholland-uk/pan-os-ansible/commit/6a3b2302349af4f1d73332cdcf65c138584e69bd))
* **panos_address_object:** Add `gathered_filter` ([41eb4e6](https://github.com/jamesholland-uk/pan-os-ansible/commit/41eb4e674beb17361252f549a38c54fd79dc3fe3))
* **panos_administrator:** Add `gathered_filter` ([bb96343](https://github.com/jamesholland-uk/pan-os-ansible/commit/bb96343278255472d148d92c0bbe7ff35720763e))
* **panos_aggregate_interface:** Add `gathered_filter` ([d0f3565](https://github.com/jamesholland-uk/pan-os-ansible/commit/d0f356589c7f5cbba42f9e38a8aa457e5eb1768c))
* **panos_aggregate_interface:** Fast failover for LACP on aggregate network interfaces ([#423](https://github.com/jamesholland-uk/pan-os-ansible/issues/423)) ([ad89bcd](https://github.com/jamesholland-uk/pan-os-ansible/commit/ad89bcd46ec46b5b1cb6d6363f8f13db0ba5655f))
* **panos_application_filter:** Add `gathered_filter` ([dd13a94](https://github.com/jamesholland-uk/pan-os-ansible/commit/dd13a947d8c756e06acd730de77f7934233cc51a))
* **panos_application_group:** Add `gathered_filter` ([4364945](https://github.com/jamesholland-uk/pan-os-ansible/commit/436494576ff3584a0f200681f74eb481854d08bf))
* **panos_application_object:** Add `gathered_filter` ([61ce619](https://github.com/jamesholland-uk/pan-os-ansible/commit/61ce61950d1aa8c8c33a81cd78a50fb221a89025))
* **panos_bgp_aggregate:** Add `gathered_filter` ([c8f33b5](https://github.com/jamesholland-uk/pan-os-ansible/commit/c8f33b56073ddd903cb263ce1f40242fab94ce0b))
* **panos_bgp_auth:** Add `gathered_filter` ([d16ce2a](https://github.com/jamesholland-uk/pan-os-ansible/commit/d16ce2a93396a8e353cfc31456fc4868030cb438))
* **panos_bgp_dampening:** Add `gathered_filter` ([e1e3aea](https://github.com/jamesholland-uk/pan-os-ansible/commit/e1e3aea47d56f47455c6720269e2bc2e7fc9c1a9))
* **panos_bgp_peer:** Add `gathered_filter` ([b1bfcb6](https://github.com/jamesholland-uk/pan-os-ansible/commit/b1bfcb64fb55154ae8657bf303e80dc27ed2a1d2))
* **panos_bgp_peer_group:** Add `gathered_filter` ([0f1ada7](https://github.com/jamesholland-uk/pan-os-ansible/commit/0f1ada773c7c21f631d39d87de42da87c0b779a0))
* **panos_bgp_redistribute:** Add `gathered_filter` ([1e061d0](https://github.com/jamesholland-uk/pan-os-ansible/commit/1e061d0e85553d04b03ea08af1ade75913af3234))
* **panos_custom_url_category:** Add `gathered_filter` ([2a746a9](https://github.com/jamesholland-uk/pan-os-ansible/commit/2a746a9070e2e7d9100de1ecb5fe3ec3e74a7e5b))
* **panos_decryption_rule:** Add `gathered_filter` ([ae52d5c](https://github.com/jamesholland-uk/pan-os-ansible/commit/ae52d5c8b5896df01c6f0dd19e189de6a5c4e19e))
* **panos_device_group:** Add `gathered_filter` ([99bf61a](https://github.com/jamesholland-uk/pan-os-ansible/commit/99bf61aa66473b88a99f3ae03f9e52f0c4b1ec6b))
* **panos_dhcp:** Add `gathered_filter` ([75ca8a2](https://github.com/jamesholland-uk/pan-os-ansible/commit/75ca8a20a1b2a276bfc75d9dc43e1fd92c9a1302))
* **panos_dhcp_relay:** Add `gathered_filter` ([0bd9a46](https://github.com/jamesholland-uk/pan-os-ansible/commit/0bd9a463ca5935b71d2d85179872143cf9e6bd58))
* **panos_dhcp_relay:** New module for DHCP Relay ([#323](https://github.com/jamesholland-uk/pan-os-ansible/issues/323)) ([ec90b6d](https://github.com/jamesholland-uk/pan-os-ansible/commit/ec90b6d27b018cf7da624f970eeb758e0b10ec46)), closes [#304](https://github.com/jamesholland-uk/pan-os-ansible/issues/304) [#318](https://github.com/jamesholland-uk/pan-os-ansible/issues/318)
* **panos_dhcp_relay_ipv6_address:** Add `gathered_filter` ([651d5fa](https://github.com/jamesholland-uk/pan-os-ansible/commit/651d5fa8507efad39f91c1117c1b011f4dce0f38))
* **panos_dynamic_user_group:** Add `gathered_filter` ([2f53fdc](https://github.com/jamesholland-uk/pan-os-ansible/commit/2f53fdc10e0916820ea7595ec31153c795c4f681))
* **panos_email_profile:** Add `gathered_filter` ([8503a82](https://github.com/jamesholland-uk/pan-os-ansible/commit/8503a823870d0ca0a40f616988337fd08521adb6))
* **panos_email_server:** Add `gathered_filter` ([812de38](https://github.com/jamesholland-uk/pan-os-ansible/commit/812de385ed443a49e7964382e6c40eea776f78a6))
* **panos_export:** Create directory if it doesn't exist ([#434](https://github.com/jamesholland-uk/pan-os-ansible/issues/434)) ([9422af0](https://github.com/jamesholland-uk/pan-os-ansible/commit/9422af0b17d1d534c73391cc95640ad6dea3d824))
* **panos_gre_tunnel:** Add `gathered_filter` ([864e4cc](https://github.com/jamesholland-uk/pan-os-ansible/commit/864e4cc2e0bd0cb93a7c22e9e7191e395e57462b))
* **panos_http_profile:** Add `gathered_filter` ([c493ce8](https://github.com/jamesholland-uk/pan-os-ansible/commit/c493ce8f7642d4048da42c8be3ab13e590a7f751))
* **panos_http_profile:** Decrypt and GP for HTTP profiles ([#427](https://github.com/jamesholland-uk/pan-os-ansible/issues/427)) ([f6c86d9](https://github.com/jamesholland-uk/pan-os-ansible/commit/f6c86d9d592ea7e4b17d7e4186ffb18c2349e359))
* **panos_http_profile_header:** Add `gathered_filter` ([deda1f3](https://github.com/jamesholland-uk/pan-os-ansible/commit/deda1f3aabc824127f9fb106b588984b72f372d6))
* **panos_http_profile_param:** Add `gathered_filter` ([814071f](https://github.com/jamesholland-uk/pan-os-ansible/commit/814071f14c2d13b28ef644c2cdf2ac26db47b93d))
* **panos_ike_crypto_profile:** Add `gathered_filter` ([cd41ef0](https://github.com/jamesholland-uk/pan-os-ansible/commit/cd41ef05a4d444901c726ba546b9297f808c5003))
* **panos_ike_crypto_profile:** Add additional parameter values ([#327](https://github.com/jamesholland-uk/pan-os-ansible/issues/327)) ([f12b2b9](https://github.com/jamesholland-uk/pan-os-ansible/commit/f12b2b969c60e03f7c35c63757da883ebf6e5e50)), closes [#315](https://github.com/jamesholland-uk/pan-os-ansible/issues/315)
* **panos_ike_gateway:** Add `gathered_filter` ([7813798](https://github.com/jamesholland-uk/pan-os-ansible/commit/781379899b26109d231f7dc51d0f5a17d99cca1a))
* **panos_import:** Add private key blocking to keypair import ([#417](https://github.com/jamesholland-uk/pan-os-ansible/issues/417)) ([3fd5bac](https://github.com/jamesholland-uk/pan-os-ansible/commit/3fd5bacdd0324ab636a0456f19993d588f900dcb))
* **panos_interface:** Add `gathered_filter` ([6406d44](https://github.com/jamesholland-uk/pan-os-ansible/commit/6406d44e9d50863d9ce561b7a743fef0d6c25a19))
* **panos_ipsec_ipv4_proxyid:** Add `gathered_filter` ([37adb74](https://github.com/jamesholland-uk/pan-os-ansible/commit/37adb74cda7322372ea91469858d8eee6a8478df))
* **panos_ipsec_tunnel:** Add `gathered_filter` ([c48c37c](https://github.com/jamesholland-uk/pan-os-ansible/commit/c48c37cb9936ff253d3678d79ade06638c5d5427))
* **panos_ipv6_address:** Add `gathered_filter` ([47c66a7](https://github.com/jamesholland-uk/pan-os-ansible/commit/47c66a7329c9505c668ae81722dc0ceade569684))
* **panos_l2_subinterface:** Add `gathered_filter` ([3886738](https://github.com/jamesholland-uk/pan-os-ansible/commit/3886738acbe8068f4b8a482b07fbd33822a0008a))
* **panos_l3_subinterface:** Add `gathered_filter` ([6e39162](https://github.com/jamesholland-uk/pan-os-ansible/commit/6e391625eba85544599f8609b39ac977648b5b73))
* **panos_log_forwarding_profile:** Add `gathered_filter` ([62e4cc5](https://github.com/jamesholland-uk/pan-os-ansible/commit/62e4cc5bbb787d2e4444d8e237e70580cb41e9c7))
* **panos_log_forwarding_profile_match_list:** Add `gathered_filter` ([8d51183](https://github.com/jamesholland-uk/pan-os-ansible/commit/8d511837879dc49eacb2300ed98a1fb62ebe439e))
* **panos_log_forwarding_profile_match_list:** Add decryption log-type to log forwarding ([#429](https://github.com/jamesholland-uk/pan-os-ansible/issues/429)) ([a1dab0a](https://github.com/jamesholland-uk/pan-os-ansible/commit/a1dab0a2b14f3ba1fa566161ce1a3f28819683cb))
* **panos_software:** name config load option ([#398](https://github.com/jamesholland-uk/pan-os-ansible/issues/398)) ([378d5a6](https://github.com/jamesholland-uk/pan-os-ansible/commit/378d5a679463918dd2e635f20ba0b086f50feb97))
* Add per-admin parameter to Panorama push ([#366](https://github.com/jamesholland-uk/pan-os-ansible/issues/366)) ([09d661e](https://github.com/jamesholland-uk/pan-os-ansible/commit/09d661e1535dea92ae48310358f4a7558229550f)), closes [#361](https://github.com/jamesholland-uk/pan-os-ansible/issues/361)
* **panos_ipsec_profile:** Add `gathered_filter` ([c1c725a](https://github.com/jamesholland-uk/pan-os-ansible/commit/c1c725a2eb81df898f5fd1746b40bee1f84cf451))
* **panos_log_forwarding_profile_match_list_action:** Add `gathered_filter` ([4f60414](https://github.com/jamesholland-uk/pan-os-ansible/commit/4f604141884d0978ba0e0eb214cefbb69d0cd546))
* **panos_loopback_interface:** Add `gathered_filter` ([b69c3b4](https://github.com/jamesholland-uk/pan-os-ansible/commit/b69c3b44df03d36ab917cc32ad7804f5fb5cc554))
* **panos_management_profile:** Add `gathered_filter` ([2371f70](https://github.com/jamesholland-uk/pan-os-ansible/commit/2371f700bfcc8ff3c2319985c60642a4aad7195e))
* **panos_nat_rule:** Module is deprecated in favor of `panos_nat_rule2` ([bc3c4f9](https://github.com/jamesholland-uk/pan-os-ansible/commit/bc3c4f996c25e6ab804bd1133ed7095ca68b8d04))
* **panos_nat_rule_facts:** Module is deprecated ([ce08e3d](https://github.com/jamesholland-uk/pan-os-ansible/commit/ce08e3d93466a4de3724d6287f185fe701bc63ec))
* **panos_nat_rule2:** Add `gathered_filter` ([369dbf4](https://github.com/jamesholland-uk/pan-os-ansible/commit/369dbf47b680a95feb8b5cf7ab031a59ae61f976))
* **panos_object_facts:** Module is deprecated ([dfb48a3](https://github.com/jamesholland-uk/pan-os-ansible/commit/dfb48a34aae18600511bb37f0b4ac2b033d56761))
* **panos_op:** Add `ignore_disconnect` param ([1eceacf](https://github.com/jamesholland-uk/pan-os-ansible/commit/1eceacf0bd026fac821fcc0a5f84b2aae235dfbd)), closes [#183](https://github.com/jamesholland-uk/pan-os-ansible/issues/183) [#331](https://github.com/jamesholland-uk/pan-os-ansible/issues/331)
* **panos_pbf_rule:** Add `gathered_filter` ([b13fb99](https://github.com/jamesholland-uk/pan-os-ansible/commit/b13fb99c684b393d6e543c85bb361bf8ba8cd717))
* **panos_pg:** Add `gathered_filter` ([783c043](https://github.com/jamesholland-uk/pan-os-ansible/commit/783c043799970f8838b27bdee065fe8ade0278dc))
* **panos_redistribution:** Add `gathered_filter` ([5a5ef22](https://github.com/jamesholland-uk/pan-os-ansible/commit/5a5ef22b39940752250dbb4a16e4d362ec2b5752))
* **panos_region:** Add `gathered_filter` ([caf289e](https://github.com/jamesholland-uk/pan-os-ansible/commit/caf289ef8856f395ef9f42b438fd76ed2c9038aa))
* **panos_schedule_object:** Add `gathered_filter` ([0458441](https://github.com/jamesholland-uk/pan-os-ansible/commit/04584412adb23782edf4d73af6fc1e7edfe7c553))
* **panos_security_rule:** Add `gathered_filter` ([1e6f2af](https://github.com/jamesholland-uk/pan-os-ansible/commit/1e6f2afd8c2ceb9543284b0868f0bab0f5d34fb4))
* **panos_security_rule_facts:** Module is deprecated ([ea71428](https://github.com/jamesholland-uk/pan-os-ansible/commit/ea714281d6e51af8a4ae346e278a1476d3e991b0))
* **panos_service_group:** Add `gathered_filter` ([1abba4a](https://github.com/jamesholland-uk/pan-os-ansible/commit/1abba4a0b281f24da51f1f53557c1637a9c3a9cd))
* **panos_service_object:** Add `gathered_filter` ([f808bee](https://github.com/jamesholland-uk/pan-os-ansible/commit/f808bee723bd2abebbd2734114305982da435dc7))
* **panos_service_object:** Add new params for overrides ([#328](https://github.com/jamesholland-uk/pan-os-ansible/issues/328)) ([ff91d9c](https://github.com/jamesholland-uk/pan-os-ansible/commit/ff91d9c361149d57332825e7e5ca40e4e7332a8b))
* **panos_snmp_profile:** Add `gathered_filter` ([87a1ad0](https://github.com/jamesholland-uk/pan-os-ansible/commit/87a1ad089cffb9a5e5cc6e8609ba2830ddb4ce7e))
* **panos_snmp_v2c_server:** Add `gathered_filter` ([c377cdc](https://github.com/jamesholland-uk/pan-os-ansible/commit/c377cdc514f6f6846456a96142e841ea5990f2d6))
* **panos_snmp_v3_server:** Add `gathered_filter` ([834901c](https://github.com/jamesholland-uk/pan-os-ansible/commit/834901c634d2f609eae90779baa83269e8f89806))
* **panos_software:** Add `perform_software_check` module param ([ab0b40c](https://github.com/jamesholland-uk/pan-os-ansible/commit/ab0b40c8245e89d08db44788637c53c44e8cd27b)), closes [#322](https://github.com/jamesholland-uk/pan-os-ansible/issues/322)
* **panos_static_route:** Add `gathered_filter` ([195b5e4](https://github.com/jamesholland-uk/pan-os-ansible/commit/195b5e429bf9372a5b251540cc71287ed479f949))
* **panos_syslog_profile:** Add `gathered_filter` ([40dc843](https://github.com/jamesholland-uk/pan-os-ansible/commit/40dc843af7a6306a7fd1afad57a2ed027d49b1d0))
* **panos_syslog_server:** Add `gathered_filter` ([3f1f966](https://github.com/jamesholland-uk/pan-os-ansible/commit/3f1f96627fb8128775cc1e1790a2431b954abdd7))
* **panos_tag_object:** Add network resource module states; add param `gathered_filter` ([31606e3](https://github.com/jamesholland-uk/pan-os-ansible/commit/31606e366e4d8d31d1753be405dff3e3c3769d34))
* **panos_template:** Add `gathered_filter` ([d10d136](https://github.com/jamesholland-uk/pan-os-ansible/commit/d10d1361aa3822d2f4d9409fa13e485e9ab5a853))
* **panos_template_stack:** Add `gathered_filter` ([d61a326](https://github.com/jamesholland-uk/pan-os-ansible/commit/d61a3260ceb187ba1b553715f1d6d1528bbe3414))
* **panos_template_variable:** Add `gathered_filter` ([8c1fea2](https://github.com/jamesholland-uk/pan-os-ansible/commit/8c1fea26aa70b61dd7c6ffd176590041d2e9393b))
* **panos_tunnel:** Add `gathered_filter` ([9f3b08c](https://github.com/jamesholland-uk/pan-os-ansible/commit/9f3b08c6c249d1a957cbe96b6cce8f8c8929b6b8))
* **panos_userid:** Add timeout to login ([d407938](https://github.com/jamesholland-uk/pan-os-ansible/commit/d4079388d78899915268d3da1bf97e20ec9e89aa)), closes [#283](https://github.com/jamesholland-uk/pan-os-ansible/issues/283)
* **panos_virtual_router:** Add `gathered_filter` ([6857369](https://github.com/jamesholland-uk/pan-os-ansible/commit/68573695c41a49dace925967837db98c4f29d2ed))
* **panos_virtual_router_facts:** Module is deprecated ([01306b5](https://github.com/jamesholland-uk/pan-os-ansible/commit/01306b51a2ee4653278597ca4ace5aea2ba5da9d))
* **panos_virtual_wire:** Add network resource module states ([532c36c](https://github.com/jamesholland-uk/pan-os-ansible/commit/532c36cdc029f4158d4c283e42d95a9a5912fa05))
* **panos_virual_wire:** Add `gathered_filter` ([e400f2d](https://github.com/jamesholland-uk/pan-os-ansible/commit/e400f2db4da01aa67aab4918526a17c5b7c9b398))
* **panos_vlan:** Add `gathered_filter` ([ec7172e](https://github.com/jamesholland-uk/pan-os-ansible/commit/ec7172e0b323df1e90bc8c736a0361b258022907))
* **panos_vlan:** Add network resource module states ([abe3977](https://github.com/jamesholland-uk/pan-os-ansible/commit/abe3977803d03e4b22dd0599330ca1a0f0cf58c7))
* **panos_vlan_interface:** Add `gathered_filter` ([397785b](https://github.com/jamesholland-uk/pan-os-ansible/commit/397785b9707714c67d1ce4091e798a572ff05c66))
* **panos_zone:** Add `gathered_filter` ([305a8e3](https://github.com/jamesholland-uk/pan-os-ansible/commit/305a8e3e2c829f6494ee4f146bcd4920dbe214b8))
* **panos_zone_facts:** Module is deprecated ([47730a7](https://github.com/jamesholland-uk/pan-os-ansible/commit/47730a7387378e8337a313f430357207c42a92c8))
* Add `panos_decryption_rule` ([#329](https://github.com/jamesholland-uk/pan-os-ansible/issues/329)) ([cd61bc8](https://github.com/jamesholland-uk/pan-os-ansible/commit/cd61bc8bbbb7b9850880389d0f5473985da492da))
* Add `panos_dhcp_relay_ipv6_address` ([0231e6d](https://github.com/jamesholland-uk/pan-os-ansible/commit/0231e6dba91948699d0002916b23ecf4ab5835c1))
* Add `panos_dhcp` ([2046d5f](https://github.com/jamesholland-uk/pan-os-ansible/commit/2046d5f1b5d5077f6535c77916abf2284d6df90b))
* Add `panos_nat_rule2` ([#330](https://github.com/jamesholland-uk/pan-os-ansible/issues/330)) ([ba8a5ac](https://github.com/jamesholland-uk/pan-os-ansible/commit/ba8a5ac25782998a0acc15899bffd550d789154c))
* Add `uuid` to policy rules ([31fbcd3](https://github.com/jamesholland-uk/pan-os-ansible/commit/31fbcd34cb959ec8a6d49274c7d9987fe8370a8d))
* **panos_address_group:** Add network resource module states ([9d8a25c](https://github.com/jamesholland-uk/pan-os-ansible/commit/9d8a25c4d46a5729c756836b20b6ccd9ad08c1c6))
* **panos_address_object:** Add network resource module state support ([589177c](https://github.com/jamesholland-uk/pan-os-ansible/commit/589177c5249ac1fb66f673f298119cdd3f461d11))
* **panos_administrator:** Add network resource module state support ([ab61249](https://github.com/jamesholland-uk/pan-os-ansible/commit/ab61249ff91131909cd4cc4d70f93d07d9e94bb7))
* **panos_aggregate_interface:** Add network resource module state support ([e82093d](https://github.com/jamesholland-uk/pan-os-ansible/commit/e82093d029d2d3b2d86692e46e2ce2109d6a3564))
* **panos_application_filter:** Add network resource module state support; corrected type of `category`, `subcategory`, `technology` and `risk` to `list` ([16e9431](https://github.com/jamesholland-uk/pan-os-ansible/commit/16e943198f24596e310ec724c1e97fc7984af2cd))
* **panos_application_group:** Add network resource module states ([e587cd9](https://github.com/jamesholland-uk/pan-os-ansible/commit/e587cd9905b98e4136b737fdf27feaf2e3d8fe3c))
* **panos_application_object:** Add network resource module support; add new params `default_type`, `default_port`, `default_ip_protocol`, `default_icmp_type`, `default_icmp_code`; correct `risk` to type `int` ([c1c6f3f](https://github.com/jamesholland-uk/pan-os-ansible/commit/c1c6f3f7539ed71239a54600c62b0983f4c9cf54))
* **panos_bgp_aggregate:** Add network resource module states ([31b92f1](https://github.com/jamesholland-uk/pan-os-ansible/commit/31b92f10011a4b5619293dd3bfa20735be5e8571))
* Add `panos_template_stack` ([#255](https://github.com/jamesholland-uk/pan-os-ansible/issues/255)) ([59f1c21](https://github.com/jamesholland-uk/pan-os-ansible/commit/59f1c2138609d5e7b919a00976c10cbb26b78428))
* Add `panos_template_variable` ([#256](https://github.com/jamesholland-uk/pan-os-ansible/issues/256)) ([6e6cc58](https://github.com/jamesholland-uk/pan-os-ansible/commit/6e6cc582c58fe5e08ac6e5a4d25c3a79e91a8d58)), closes [#248](https://github.com/jamesholland-uk/pan-os-ansible/issues/248)
* Add audit comment to panos_nat_rule ([c29314e](https://github.com/jamesholland-uk/pan-os-ansible/commit/c29314ea91f094d98be6f3b6c5b5deb9aca52dbb))
* Add audit comment to panos_pbf_rule ([640bd25](https://github.com/jamesholland-uk/pan-os-ansible/commit/640bd2510a1267f3a847c80939cb96e1f99da5be))
* Add device group support ([#250](https://github.com/jamesholland-uk/pan-os-ansible/issues/250)) ([26a991c](https://github.com/jamesholland-uk/pan-os-ansible/commit/26a991c51fac3311467dc27b0008f3b13bad08f0)), closes [#102](https://github.com/jamesholland-uk/pan-os-ansible/issues/102)
* Add group_tag to panos_nat_rule ([34d4a4b](https://github.com/jamesholland-uk/pan-os-ansible/commit/34d4a4bc9647493d47901d090391d76ecc8615ab)), closes [#244](https://github.com/jamesholland-uk/pan-os-ansible/issues/244)
* Add group_tag to panos_pbf_rule ([f0ba7ed](https://github.com/jamesholland-uk/pan-os-ansible/commit/f0ba7ed7eddedcda91ee4f6ff2b8004b7083f5d0)), closes [#244](https://github.com/jamesholland-uk/pan-os-ansible/issues/244)
* Add group_tag to panos_security_rule ([63148d9](https://github.com/jamesholland-uk/pan-os-ansible/commit/63148d9fe135f299e49d7dd223504d0310e803cd)), closes [#244](https://github.com/jamesholland-uk/pan-os-ansible/issues/244)
* Add NAT rule dynamic dest xlate support ([#251](https://github.com/jamesholland-uk/pan-os-ansible/issues/251)) ([5db35d0](https://github.com/jamesholland-uk/pan-os-ansible/commit/5db35d0839ead83333f2092490cc60701c6e7287)), closes [#146](https://github.com/jamesholland-uk/pan-os-ansible/issues/146)
* Add panos_template ([#254](https://github.com/jamesholland-uk/pan-os-ansible/issues/254)) ([f122df8](https://github.com/jamesholland-uk/pan-os-ansible/commit/f122df8e8ee77f450fc09eb04f5d6a63a10654da))
* Add support for certain network resource module states ([9072bad](https://github.com/jamesholland-uk/pan-os-ansible/commit/9072bada5f51fa72d2a30a58adf19f2b45d74fad))
* **panos_aggregate_interface:** Support LACP ([#119](https://github.com/jamesholland-uk/pan-os-ansible/issues/119)) ([e015bb5](https://github.com/jamesholland-uk/pan-os-ansible/commit/e015bb518674935ff8022e6bfa93b61678110e5e)), closes [#66](https://github.com/jamesholland-uk/pan-os-ansible/issues/66)
* **panos_bgp_auth:** Add network resource module states ([e00b883](https://github.com/jamesholland-uk/pan-os-ansible/commit/e00b883eea065f87ad665e297951ea463cacde9f))
* **panos_bgp_dampening:** Add network resource module states ([536d3e1](https://github.com/jamesholland-uk/pan-os-ansible/commit/536d3e14d1dfd22c22c826f6ecf379c6c5b34dab))
* **panos_bgp_peer:** Add network resource module states ([17e31b0](https://github.com/jamesholland-uk/pan-os-ansible/commit/17e31b056c5d73f763e36a44bb9192d5e6aa2711))
* **panos_bgp_peer_group:** Add network resource module states ([67e9c6f](https://github.com/jamesholland-uk/pan-os-ansible/commit/67e9c6fa471ffe1ffa1b3fef472074cc5a27469a))
* **panos_bgp_redistribute:** Add network resource module states ([e1127e9](https://github.com/jamesholland-uk/pan-os-ansible/commit/e1127e932106ee6c464853f9a730ed6dcd0f919d))
* **panos_check:** Check status of autocommit job for better accuracy. ([#187](https://github.com/jamesholland-uk/pan-os-ansible/issues/187)) ([87bdb65](https://github.com/jamesholland-uk/pan-os-ansible/commit/87bdb6529ffa3229660b0b26a837bba74bd8674e))
* **panos_custom_url_category:** Add network resource module states ([df629a9](https://github.com/jamesholland-uk/pan-os-ansible/commit/df629a9d718965fce8f9fac00a251f328ffe12de))
* **panos_custom_url_category:** Support description field ([7804fa6](https://github.com/jamesholland-uk/pan-os-ansible/commit/7804fa613f5421eb6b91767f4239458ed989a7d3))
* **panos_device_group:** Add network resource module states ([b74f6c3](https://github.com/jamesholland-uk/pan-os-ansible/commit/b74f6c37de64f577b51309f7ed0dc2b91fd7c793))
* **panos_dynamic_user_group:** Add network resource module states ([c32f2ea](https://github.com/jamesholland-uk/pan-os-ansible/commit/c32f2ea25f1279c5d61028ebcd23cad201685e44))
* **panos_email_profile:** Add network resource module states ([f9b6113](https://github.com/jamesholland-uk/pan-os-ansible/commit/f9b6113cdeeccea4affd709ff43e62fa76b22510))
* **panos_email_server:** Add network resource module states ([ec0eb4e](https://github.com/jamesholland-uk/pan-os-ansible/commit/ec0eb4ef890eea93be9918802d700a3def76936e))
* **panos_email_server:** Add protocol ([#231](https://github.com/jamesholland-uk/pan-os-ansible/issues/231)) ([b4a0b1a](https://github.com/jamesholland-uk/pan-os-ansible/commit/b4a0b1ab40f14170c39d8bd7d0ac25bb2077414a))
* **panos_gre_tunnel:** Add network resource module states ([a1a49f2](https://github.com/jamesholland-uk/pan-os-ansible/commit/a1a49f2ceca16b1b30d6d5de1695823e9668dc6a))
* **panos_http_profile:** Add network resource module states ([2eb2569](https://github.com/jamesholland-uk/pan-os-ansible/commit/2eb256979b704dfa1352012a78072abb4aadaa37))
* **panos_http_profile_header:** Add network resource module states ([704e85d](https://github.com/jamesholland-uk/pan-os-ansible/commit/704e85dc8452f7a54687ad734ebea86e2bff8560))
* **panos_http_profile_param:** Add network resource module states ([0a4b6a4](https://github.com/jamesholland-uk/pan-os-ansible/commit/0a4b6a4066cc8dc9855b35750baaec50541fbfe7))
* **panos_http_server:** Add network resource module states ([bcb0d01](https://github.com/jamesholland-uk/pan-os-ansible/commit/bcb0d01d9655e49db6bc8a5587201209823eac7d))
* **panos_ike_crypto_profile:** Add network resource module states ([ca3a7e9](https://github.com/jamesholland-uk/pan-os-ansible/commit/ca3a7e9a3ab5d89656c53bc49cf4bfed7fb4f7c5))
* **panos_ike_gateway:** Add fqdn to peer_address_type ([#105](https://github.com/jamesholland-uk/pan-os-ansible/issues/105)) ([6c02bdd](https://github.com/jamesholland-uk/pan-os-ansible/commit/6c02bdd3fd0a591b5ad5e31573eeaf56a3ea82c8)), closes [#10](https://github.com/jamesholland-uk/pan-os-ansible/issues/10)
* **panos_ike_gateway:** Add network resource module states ([0316aa0](https://github.com/jamesholland-uk/pan-os-ansible/commit/0316aa07851df5f6903563233dc2b63fa0f80d39))
* **panos_import:** Add additional import options ([#121](https://github.com/jamesholland-uk/pan-os-ansible/issues/121)) ([dab471a](https://github.com/jamesholland-uk/pan-os-ansible/commit/dab471a0cfbc689dab94d35ad9686a5d9a9072f6)), closes [#68](https://github.com/jamesholland-uk/pan-os-ansible/issues/68)
* **panos_import:** Add SAML metadata profile ([#213](https://github.com/jamesholland-uk/pan-os-ansible/issues/213)) ([a55dc97](https://github.com/jamesholland-uk/pan-os-ansible/commit/a55dc97622743392b937902533deb7c9325043e8))
* **panos_import:** Support import to template ([#225](https://github.com/jamesholland-uk/pan-os-ansible/issues/225)) ([82db7fe](https://github.com/jamesholland-uk/pan-os-ansible/commit/82db7fea0908382d451abae25531f4a6bdbc23a6))
* **panos_interface:** Add network resource module states ([0c6e2ac](https://github.com/jamesholland-uk/pan-os-ansible/commit/0c6e2ac044eb3bd07a743b75c283b80d5e9ac34b))
* **panos_ipsec_ipv4_proxyid:** Add network resource module states ([120d26c](https://github.com/jamesholland-uk/pan-os-ansible/commit/120d26cc343b160041a4c0cdc363e0fc798e20b4))
* **panos_ipsec_profile:** Add network resource module states ([716e5c4](https://github.com/jamesholland-uk/pan-os-ansible/commit/716e5c434fb921a0c48e813ef10863e3da840625))
* **panos_ipsec_tunnel:** Add network resource module states ([98bb16e](https://github.com/jamesholland-uk/pan-os-ansible/commit/98bb16effe3c06e1aaac91e77c73cde65d74f00b))
* **panos_ipv6_address:** Add network resource module states ([be0244f](https://github.com/jamesholland-uk/pan-os-ansible/commit/be0244fa7453afe6ebfabecbad16027db61a19c4))
* **panos_l2_subinterface:** Add network resource module states ([2ff6d18](https://github.com/jamesholland-uk/pan-os-ansible/commit/2ff6d18ae21a6efa06f9ebae21e4626f99d956ce))
* **panos_l3_subinterface:** Add network resource module states ([a44bd3f](https://github.com/jamesholland-uk/pan-os-ansible/commit/a44bd3f57a13ff0e88eabc9799cca60bf0dd62ee))
* **panos_log_forwarding_profile:** Add network resource module states ([14b435e](https://github.com/jamesholland-uk/pan-os-ansible/commit/14b435e06b3dd2a4c39ded7375c54bac6491b5d1))
* **panos_log_forwarding_profile_match_list:** Add network resource module states ([736f181](https://github.com/jamesholland-uk/pan-os-ansible/commit/736f181a7ab64ab4247af91e56805f94ba17401f))
* **panos_log_forwarding_profile_match_list_action:** Add network resource module states ([b1dbfcf](https://github.com/jamesholland-uk/pan-os-ansible/commit/b1dbfcfb69073c38beb225a98b1c49e7b32c15ff))
* **panos_loopback_interface:** Add network resource module states ([13e02c6](https://github.com/jamesholland-uk/pan-os-ansible/commit/13e02c6edf5047b59b34f7c88bdb2211cda5abf7))
* **panos_management_profile:** Add network resource module states ([11bf248](https://github.com/jamesholland-uk/pan-os-ansible/commit/11bf2487be6960402e2007a907ccd94d5daeeb73))
* **panos_mgtconfig:** Added template support ([#268](https://github.com/jamesholland-uk/pan-os-ansible/issues/268)) ([51008cb](https://github.com/jamesholland-uk/pan-os-ansible/commit/51008cb27ef0ab2a129ffbc7cc9948d5a432d91e))
* **panos_object_facts:** Add support for Custom URL Categories ([#249](https://github.com/jamesholland-uk/pan-os-ansible/issues/249)) ([30be003](https://github.com/jamesholland-uk/pan-os-ansible/commit/30be003d2eea5df3a9502577d6b021ef1dd0a60d))
* **panos_object_facts:** Support applications and application groups ([8d9c138](https://github.com/jamesholland-uk/pan-os-ansible/commit/8d9c13867d8c1d52efc143d60c2c5b46f7e54585))
* **panos_security_rule:** Add audit comment ([#229](https://github.com/jamesholland-uk/pan-os-ansible/issues/229)) ([bae2483](https://github.com/jamesholland-uk/pan-os-ansible/commit/bae2483c33b1c0a710a15226656660bec87b7d9a)), closes [#228](https://github.com/jamesholland-uk/pan-os-ansible/issues/228)
* **panos_tag_object:** Add new colors ([#111](https://github.com/jamesholland-uk/pan-os-ansible/issues/111)) ([#234](https://github.com/jamesholland-uk/pan-os-ansible/issues/234)) ([1703f29](https://github.com/jamesholland-uk/pan-os-ansible/commit/1703f2967aeeaa10fe8b7de47d69ae9b77fa1aab))
* Add httpapi connection ([#223](https://github.com/jamesholland-uk/pan-os-ansible/issues/223)) ([5d11cfc](https://github.com/jamesholland-uk/pan-os-ansible/commit/5d11cfc562504cfd0f338bbdb47fdd9b6e1c4155))
* add panos_application_object ([#81](https://github.com/jamesholland-uk/pan-os-ansible/issues/81)) ([b4e04d9](https://github.com/jamesholland-uk/pan-os-ansible/commit/b4e04d93eda4f2456d215fa36750efb7e391ae06))
* Add panos_config_element ([be878d4](https://github.com/jamesholland-uk/pan-os-ansible/commit/be878d4be2f3e367bcf20242cc7b60eddbb081d3)), closes [#219](https://github.com/jamesholland-uk/pan-os-ansible/issues/219)
* Add panos_dynamic_updates ([#189](https://github.com/jamesholland-uk/pan-os-ansible/issues/189)) ([bb2f2ed](https://github.com/jamesholland-uk/pan-os-ansible/commit/bb2f2ed285ac235ba736358632b774eb5aadec01)), closes [#49](https://github.com/jamesholland-uk/pan-os-ansible/issues/49)
* Also return the XML when `state=gathered` ([559ccf1](https://github.com/jamesholland-uk/pan-os-ansible/commit/559ccf177d73354ace3114f1df1629c014deb6ea))
* Enhanced checks for dependent python libraries ([de34ae9](https://github.com/jamesholland-uk/pan-os-ansible/commit/de34ae9282ef09e727e082a0d4cb32e77d2d444d)), closes [#324](https://github.com/jamesholland-uk/pan-os-ansible/issues/324)
* **panos_nat_rule:** Support target, negate_target ([#179](https://github.com/jamesholland-uk/pan-os-ansible/issues/179)) ([dffedd3](https://github.com/jamesholland-uk/pan-os-ansible/commit/dffedd3576563ce072f24669048fdf753f3c77d9)), closes [#175](https://github.com/jamesholland-uk/pan-os-ansible/issues/175)
* **panos_op:** Support vsys ([e5e785a](https://github.com/jamesholland-uk/pan-os-ansible/commit/e5e785ab26422b53aec555be6da35092a287c0eb))
* **panos_pbf_rule:** Add network resource module states ([ea1434b](https://github.com/jamesholland-uk/pan-os-ansible/commit/ea1434b0f8ccb85484d22b01408043c0832a6e97))
* **panos_pg:** Add network resource module states ([7bb8b84](https://github.com/jamesholland-uk/pan-os-ansible/commit/7bb8b84ce2a82e730dc9824c1cc8793e0f05faa2))
* **panos_redistribution:** Add network resource module states ([390ac8d](https://github.com/jamesholland-uk/pan-os-ansible/commit/390ac8d77fbf8acee10fe9eff5ac19a53ca545d2))
* **panos_region:** Add network resource module states ([baaacd0](https://github.com/jamesholland-uk/pan-os-ansible/commit/baaacd0f6d53ee3f9efd64c7f7a0f2181175e172))
* **panos_schedule_object:** Add network resource module states ([5e79661](https://github.com/jamesholland-uk/pan-os-ansible/commit/5e7966148afca7f918f1cb274737544c61fbe243))
* **panos_security_rule:** Add network resource module states ([195cfd9](https://github.com/jamesholland-uk/pan-os-ansible/commit/195cfd9174177bb25761f64736d0407d0e03f0c0))
* **panos_security_rule_facts:** Support 'match_rules' ([#130](https://github.com/jamesholland-uk/pan-os-ansible/issues/130)) ([ade1ba6](https://github.com/jamesholland-uk/pan-os-ansible/commit/ade1ba6103864daf95927138f94d2604cc13f0b7)), closes [#128](https://github.com/jamesholland-uk/pan-os-ansible/issues/128)
* **panos_service_group:** Add network resource module states ([5fffeee](https://github.com/jamesholland-uk/pan-os-ansible/commit/5fffeeef22804152bd017b361f59cbba8d46da70))
* **panos_service_object:** Add network resource module states ([dbd9bfd](https://github.com/jamesholland-uk/pan-os-ansible/commit/dbd9bfdc321a3f46af4c87d748f97ccdd72e735e))
* **panos_snmp_profile:** Add network resource module states ([e1e799a](https://github.com/jamesholland-uk/pan-os-ansible/commit/e1e799adbc1d4e33018686997ba6380c38e7b308))
* **panos_snmp_v2c_server:** Add network resource module states ([53fdbee](https://github.com/jamesholland-uk/pan-os-ansible/commit/53fdbeee2f1984e8e06b57e1e548aec54f9bc0c1))
* **panos_snmp_v3_server:** Add network resource module states ([083fdeb](https://github.com/jamesholland-uk/pan-os-ansible/commit/083fdebc9974e4b0f67cac2af6a05d76029c3164))
* **panos_software:** Download new base version automatically for upgrades ([#186](https://github.com/jamesholland-uk/pan-os-ansible/issues/186)) ([95516b9](https://github.com/jamesholland-uk/pan-os-ansible/commit/95516b9425ef6ee923145cb791188c56da84a806))
* **panos_software:** Only download when actually needed ([4728be7](https://github.com/jamesholland-uk/pan-os-ansible/commit/4728be766440ce612335d485ff2aa35b2d2fc169))
* **panos_static_route:** Add network resource module states ([f76b75c](https://github.com/jamesholland-uk/pan-os-ansible/commit/f76b75cb13ed50ca7c2e0c557377887f0d715107))
* **panos_syslog_profile:** Add network resource module states ([b50258e](https://github.com/jamesholland-uk/pan-os-ansible/commit/b50258ee0638801d4b3c9de5fd294e29e555e9ae))
* **panos_syslog_server:** Add network resource module states ([8c1f5aa](https://github.com/jamesholland-uk/pan-os-ansible/commit/8c1f5aa4493c2de247b17ce60747a24a9100878b))
* **panos_template:** Add network resource module states ([e3230a3](https://github.com/jamesholland-uk/pan-os-ansible/commit/e3230a378c4dae714af1c9fefdc9f01c518b2cb7))
* **panos_template_stack:** Add network resource module states ([7bd1750](https://github.com/jamesholland-uk/pan-os-ansible/commit/7bd17501b12e3b29706254f42138f3165e150a2a))
* **panos_template_variable:** Add network resource module states ([3ed3439](https://github.com/jamesholland-uk/pan-os-ansible/commit/3ed34393735fd3a06b0bd7521dcaff6e862ac254))
* **panos_tunnel:** Add network resource module states ([f396b11](https://github.com/jamesholland-uk/pan-os-ansible/commit/f396b1122a2db7c59ff9116c49b214d99b1b2577))
* **panos_virtual_router:** Add network resource module states ([40d1d70](https://github.com/jamesholland-uk/pan-os-ansible/commit/40d1d70923bd1bf39c08959c9afdd60b25e28918))
* **panos_vlan_interface:** Add network resource module states ([85f1042](https://github.com/jamesholland-uk/pan-os-ansible/commit/85f104233e93b4d1d39fa81efcc52e55b1c0cfd5))
* **panos_zone:** Add network resource module states ([419f2f2](https://github.com/jamesholland-uk/pan-os-ansible/commit/419f2f27219f0828cb00c2ccfb823f95ceaa357e))
* Add additional object modules ([#127](https://github.com/jamesholland-uk/pan-os-ansible/issues/127)) ([f294863](https://github.com/jamesholland-uk/pan-os-ansible/commit/f2948634f05ba2b8926417471ed383ce568f3613)), closes [#75](https://github.com/jamesholland-uk/pan-os-ansible/issues/75)
* add panos_custom_url_category module ([#79](https://github.com/jamesholland-uk/pan-os-ansible/issues/79)) ([73cf877](https://github.com/jamesholland-uk/pan-os-ansible/commit/73cf8779782ef0fb5ed3e9cc9e6a91951648c33d))
* helper support for pan-os-python ([#84](https://github.com/jamesholland-uk/pan-os-ansible/issues/84)) ([abd2b4b](https://github.com/jamesholland-uk/pan-os-ansible/commit/abd2b4b71ec66f980ca3eaf04da972abf1417c98))
* Migrate to pan-os-python ([d43cfe6](https://github.com/jamesholland-uk/pan-os-ansible/commit/d43cfe6c6530d00114793017b907a81fef650ff7))
* new commit modules ([#98](https://github.com/jamesholland-uk/pan-os-ansible/issues/98)) ([424c6f0](https://github.com/jamesholland-uk/pan-os-ansible/commit/424c6f042b5d32c024f9143884eda4d8989dec9b)), closes [#51](https://github.com/jamesholland-uk/pan-os-ansible/issues/51) [#52](https://github.com/jamesholland-uk/pan-os-ansible/issues/52)


### Bug Fixes

* **eda:** Make `custom_logger` argument optional ([#456](https://github.com/jamesholland-uk/pan-os-ansible/issues/456)) ([49ed307](https://github.com/jamesholland-uk/pan-os-ansible/commit/49ed3079e646072401075b68da07bd0799818e42))
* **eda:** Move EDA plugin to correct path ([#444](https://github.com/jamesholland-uk/pan-os-ansible/issues/444)) ([dc524e9](https://github.com/jamesholland-uk/pan-os-ansible/commit/dc524e93b87f0163cc3019636617198a59ebf51f))
* **event-driven ansible:** Update for Red Hat's certification checks ([#479](https://github.com/jamesholland-uk/pan-os-ansible/issues/479)) ([0fdce26](https://github.com/jamesholland-uk/pan-os-ansible/commit/0fdce2660dd357b5a5e3cde706068f89655c6a4f))
* **gathered_filter:** Fix error handling for no-value operators ([#489](https://github.com/jamesholland-uk/pan-os-ansible/issues/489)) ([351960c](https://github.com/jamesholland-uk/pan-os-ansible/commit/351960c90624b299ce8cdd35146d95bd941ed22c))
* **gathered_filter:** Update logic to cover cases of None ([#488](https://github.com/jamesholland-uk/pan-os-ansible/issues/488)) ([d2372c5](https://github.com/jamesholland-uk/pan-os-ansible/commit/d2372c5f9e3a26f047859e3feed5ab647970c631))
* **panos_admpwd:** Fix success criteria and update example in docs ([#457](https://github.com/jamesholland-uk/pan-os-ansible/issues/457)) ([9ecdb65](https://github.com/jamesholland-uk/pan-os-ansible/commit/9ecdb65bb88db4528cbae7221f4ea930a62e49c9))
* **panos_bgp_peer_group:** Fix for IBGP export next-hop options ([#459](https://github.com/jamesholland-uk/pan-os-ansible/issues/459)) ([9489fa2](https://github.com/jamesholland-uk/pan-os-ansible/commit/9489fa25b6f3f898aa6c080d6f1676c1747e073f))
* **panos_bgp_policy_rule:** Add conditional for `address_prefix` ([#340](https://github.com/jamesholland-uk/pan-os-ansible/issues/340)) ([666d78e](https://github.com/jamesholland-uk/pan-os-ansible/commit/666d78e484b95ea11348ad18ea0ebc2b9dca3073))
* **panos_commit_push:** commit_push fail messaging ([#407](https://github.com/jamesholland-uk/pan-os-ansible/issues/407)) ([6b2b370](https://github.com/jamesholland-uk/pan-os-ansible/commit/6b2b370558439a91be53c4423fbe39c5e4b66345))
* **panos_device_group:** Do not move a Device Group if state is set to gathered ([#484](https://github.com/jamesholland-uk/pan-os-ansible/issues/484)) ([93d61a7](https://github.com/jamesholland-uk/pan-os-ansible/commit/93d61a76cb81342c4ef743b7bce28e6132120288))
* **panos_export:** Fix binary exports ([#389](https://github.com/jamesholland-uk/pan-os-ansible/issues/389)) ([2666536](https://github.com/jamesholland-uk/pan-os-ansible/commit/2666536b56957273c16bed5f6a8173d15ebabe4e))
* **panos_export:** Fix export filename errors ([#360](https://github.com/jamesholland-uk/pan-os-ansible/issues/360)) ([a0f1b8f](https://github.com/jamesholland-uk/pan-os-ansible/commit/a0f1b8fcfec45566b1f404c435a125a2f6e6c149)), closes [#359](https://github.com/jamesholland-uk/pan-os-ansible/issues/359)
* **panos_ike_crypto_profile:** Fixed auth type `non-auth` for IKE profile ([#418](https://github.com/jamesholland-uk/pan-os-ansible/issues/418)) ([0a2abe8](https://github.com/jamesholland-uk/pan-os-ansible/commit/0a2abe80055982ddf2035d24f9adde36ce226a55))
* **panos_ike_crypto_profile:** Update DH group choices ([#461](https://github.com/jamesholland-uk/pan-os-ansible/issues/461)) ([8194318](https://github.com/jamesholland-uk/pan-os-ansible/commit/8194318c496f192e9eb63526cc7a13df4f1ca493))
* **panos_interface:** Fix DHCP disabled handling ([4b579be](https://github.com/jamesholland-uk/pan-os-ansible/commit/4b579becf3cc5fb5997bfdc5ea8a84ba37e3067a))
* **panos_ipsec_ipv4_proxyid:** Fix IPv4 ProxyID proto parameter ([#386](https://github.com/jamesholland-uk/pan-os-ansible/issues/386)) ([a07edad](https://github.com/jamesholland-uk/pan-os-ansible/commit/a07edad50c9755f0cd6c33fe974fe7196a3ac34d))
* **panos_ipsec_profile:** Update DH group choices ([#462](https://github.com/jamesholland-uk/pan-os-ansible/issues/462)) ([1798a3b](https://github.com/jamesholland-uk/pan-os-ansible/commit/1798a3b0ab7b4cf415d44df0c13d96cec5111252))
* **panos_l2_subinterface:** Fix netflow profile param name ([7a4063c](https://github.com/jamesholland-uk/pan-os-ansible/commit/7a4063cd7305b62eb0a19a052ae35934c12d01aa)), closes [#350](https://github.com/jamesholland-uk/pan-os-ansible/issues/350)
* **panos_l3_subinterface:** Fix DHCP disabled handling ([27eca02](https://github.com/jamesholland-uk/pan-os-ansible/commit/27eca0269b1a031b7fdb5f9963624aa7a039caa0)), closes [#335](https://github.com/jamesholland-uk/pan-os-ansible/issues/335)
* **panos_loopback_interface:** Defined `vsys_dg` before attempting to use it ([646357a](https://github.com/jamesholland-uk/pan-os-ansible/commit/646357aec5f5171c5686dd1897d840467dfb1586)), closes [#341](https://github.com/jamesholland-uk/pan-os-ansible/issues/341)
* **panos_nat_rule:** fix helper params ([#381](https://github.com/jamesholland-uk/pan-os-ansible/issues/381)) ([f1d2b13](https://github.com/jamesholland-uk/pan-os-ansible/commit/f1d2b13000471ca812aaa60276a05599af903156))
* **panos_op:** Remove `xmltodict` as a required install for this module ([0677de0](https://github.com/jamesholland-uk/pan-os-ansible/commit/0677de0de24e4970d2318a0e2c7a48581ebda427)), closes [#352](https://github.com/jamesholland-uk/pan-os-ansible/issues/352)
* **panos_security_rule:** Better handling of `hip_profiles` which is removed in newer PAN-OS versions ([77ff27d](https://github.com/jamesholland-uk/pan-os-ansible/commit/77ff27df6c7bf8fe07de593ba4b13726530c9ed9)), closes [#291](https://github.com/jamesholland-uk/pan-os-ansible/issues/291)
* **panos_security_rule_facts:** params typo ([#379](https://github.com/jamesholland-uk/pan-os-ansible/issues/379)) ([2558feb](https://github.com/jamesholland-uk/pan-os-ansible/commit/2558feb6a854ac8fe2036a19bc25e705049df216))
* **panos_software:** Modify valid sequence for downloads only ([#463](https://github.com/jamesholland-uk/pan-os-ansible/issues/463)) ([214c4bb](https://github.com/jamesholland-uk/pan-os-ansible/commit/214c4bb9f2c7a9421694f808ba8f0f83e635dca5))
* **panos_software:** Refresh device version before getting version ([#363](https://github.com/jamesholland-uk/pan-os-ansible/issues/363)) ([cce2509](https://github.com/jamesholland-uk/pan-os-ansible/commit/cce25090cc4e35bedac5d01cbd02241427383606))
* **various:** Remove unused imports for pylint testing ([#495](https://github.com/jamesholland-uk/pan-os-ansible/issues/495)) ([71aecd6](https://github.com/jamesholland-uk/pan-os-ansible/commit/71aecd6ec2128c8035e1ad40479e9c059fa27388))
* Address import pylint errors ([#391](https://github.com/jamesholland-uk/pan-os-ansible/issues/391)) ([6c81424](https://github.com/jamesholland-uk/pan-os-ansible/commit/6c814240ce16be04d62070307b91f77b3aa8e76e))
* Always import interfaces ([9fa3b6a](https://github.com/jamesholland-uk/pan-os-ansible/commit/9fa3b6a3f121d4e3dc5bfb1a8b1c2bc0b523b38e)), closes [#296](https://github.com/jamesholland-uk/pan-os-ansible/issues/296)
* CI for semantic-release ([4175aff](https://github.com/jamesholland-uk/pan-os-ansible/commit/4175aff753f98af3c41a5fc52b63a01019072b74))
* CI for upload-artifact ([09673e6](https://github.com/jamesholland-uk/pan-os-ansible/commit/09673e652f70778a6ffaa20e12d7f64bb9ee5282))
* Idempotentency change when multiple children are present ([f42650c](https://github.com/jamesholland-uk/pan-os-ansible/commit/f42650c85f06532a12c7af121c06b43f41d505fd)), closes [#319](https://github.com/jamesholland-uk/pan-os-ansible/issues/319)
* Ignore changes in uuid for policy rules ([7e0d6cb](https://github.com/jamesholland-uk/pan-os-ansible/commit/7e0d6cbbe9d2072034df5e8ae61da37fac9721cd)), closes [#310](https://github.com/jamesholland-uk/pan-os-ansible/issues/310)
* Instantiate classes that have `Name = None` when building up parent object hierarchies ([229a5e0](https://github.com/jamesholland-uk/pan-os-ansible/commit/229a5e04044b70155ec023787d7e48719ce7f694)), closes [#339](https://github.com/jamesholland-uk/pan-os-ansible/issues/339)
* Tox-compliant EDA code, and Tox checks in CI ([#453](https://github.com/jamesholland-uk/pan-os-ansible/issues/453)) ([9a50c9b](https://github.com/jamesholland-uk/pan-os-ansible/commit/9a50c9bb5e841ddfe0eeca7ea9021eb289e0e5db))
* **panos_custom_url_category:** Add minimum SDK version check ([0619dcb](https://github.com/jamesholland-uk/pan-os-ansible/commit/0619dcb5a81d8899bac85110b20077559802f072))
* Improve minimum package error message ([#271](https://github.com/jamesholland-uk/pan-os-ansible/issues/271)) ([a77a53d](https://github.com/jamesholland-uk/pan-os-ansible/commit/a77a53de947fcb18249227d1beffeed6d6b53c51))
* **panos_aggregate_interface:** Add LACP parameters ([02a52ca](https://github.com/jamesholland-uk/pan-os-ansible/commit/02a52ca193197b8224235d5e839617da67b31c37))
* **panos_custom_url_category:** Don't use type parameter ([#147](https://github.com/jamesholland-uk/pan-os-ansible/issues/147)) ([f84379f](https://github.com/jamesholland-uk/pan-os-ansible/commit/f84379fc8fe82e1688843de7b89ae14a83121a1f)), closes [#143](https://github.com/jamesholland-uk/pan-os-ansible/issues/143)
* **panos_custom_url_category:** Fix imports for pandevice ([#145](https://github.com/jamesholland-uk/pan-os-ansible/issues/145)) ([b268787](https://github.com/jamesholland-uk/pan-os-ansible/commit/b268787621cc51d4d6afa7c0882ef0b515671f66)), closes [#142](https://github.com/jamesholland-uk/pan-os-ansible/issues/142)
* **panos_custom_url_category:** Set type only on PAN-OS 9.0+ ([e94c04a](https://github.com/jamesholland-uk/pan-os-ansible/commit/e94c04a37fc3e651e9b43518aa7fe9fb6d44f1a3))
* **panos_export:** Fix export_binary ([#188](https://github.com/jamesholland-uk/pan-os-ansible/issues/188)) ([86b66cb](https://github.com/jamesholland-uk/pan-os-ansible/commit/86b66cb0022ebb52c7c01c9801dd7452dfbb6c0b)), closes [#181](https://github.com/jamesholland-uk/pan-os-ansible/issues/181)
* **panos_export:** Rename include-keys param for certificate export ([e1be0ac](https://github.com/jamesholland-uk/pan-os-ansible/commit/e1be0ac451216deebf0f4f3b869fc4658d1576ab)), closes [#163](https://github.com/jamesholland-uk/pan-os-ansible/issues/163)
* **panos_import:** Allow user specified HTTPS port ([#159](https://github.com/jamesholland-uk/pan-os-ansible/issues/159)) ([cca5de2](https://github.com/jamesholland-uk/pan-os-ansible/commit/cca5de2699b6bcf6c6e15f3a0ea9b7637fb81ea4)), closes [#154](https://github.com/jamesholland-uk/pan-os-ansible/issues/154)
* **panos_match_rule:** Fix exception on match failure ([#169](https://github.com/jamesholland-uk/pan-os-ansible/issues/169)) ([923513d](https://github.com/jamesholland-uk/pan-os-ansible/commit/923513d977510bd1ff3625716bbf475e505e0f1b)), closes [#166](https://github.com/jamesholland-uk/pan-os-ansible/issues/166)
* **panos_nat_rule:** Correct KeyError for dynamic xlate ([#267](https://github.com/jamesholland-uk/pan-os-ansible/issues/267)) ([03071b4](https://github.com/jamesholland-uk/pan-os-ansible/commit/03071b483533c8f56031cd956681063d871ca85a))
* "shared" should be allowed in panos_security_rule ([#125](https://github.com/jamesholland-uk/pan-os-ansible/issues/125)) ([fa164c7](https://github.com/jamesholland-uk/pan-os-ansible/commit/fa164c7d13fdd53b4d1188818691b944ad755753)), closes [#90](https://github.com/jamesholland-uk/pan-os-ansible/issues/90)
* Adding tags to ip address would fail ([#107](https://github.com/jamesholland-uk/pan-os-ansible/issues/107)) ([43d1af0](https://github.com/jamesholland-uk/pan-os-ansible/commit/43d1af0542e8d20a9f3f2b5c76ff2781d8891104)), closes [#48](https://github.com/jamesholland-uk/pan-os-ansible/issues/48)
* address_prefix should be list of type dict ([#117](https://github.com/jamesholland-uk/pan-os-ansible/issues/117)) ([261633b](https://github.com/jamesholland-uk/pan-os-ansible/commit/261633b9f95f1807bf18944e59fd50186f912998)), closes [#116](https://github.com/jamesholland-uk/pan-os-ansible/issues/116)
* address_prefix should be list of type dict ([#124](https://github.com/jamesholland-uk/pan-os-ansible/issues/124)) ([bd02fd0](https://github.com/jamesholland-uk/pan-os-ansible/commit/bd02fd0769f80cf568610e1ec61ef8af1334c99d)), closes [#118](https://github.com/jamesholland-uk/pan-os-ansible/issues/118)
* Do targetted updates in panos_device_group ([#253](https://github.com/jamesholland-uk/pan-os-ansible/issues/253)) ([8fa1906](https://github.com/jamesholland-uk/pan-os-ansible/commit/8fa190618bd89bfc68f156ba91ca221942647bc4)), closes [#252](https://github.com/jamesholland-uk/pan-os-ansible/issues/252)
* panos_ha should check for a config before indexing ([4d050c4](https://github.com/jamesholland-uk/pan-os-ansible/commit/4d050c4bb244de9937402e08d4c973856ebf579c)), closes [#32](https://github.com/jamesholland-uk/pan-os-ansible/issues/32)
* **panos_facts:** Fix IPv6 on subinterfaces ([#218](https://github.com/jamesholland-uk/pan-os-ansible/issues/218)) ([51e1f55](https://github.com/jamesholland-uk/pan-os-ansible/commit/51e1f55b7584aebd54fa5b1b766d3aa7faf1af27))
* **panos_facts:** Fix Panorama HA data collection ([#140](https://github.com/jamesholland-uk/pan-os-ansible/issues/140)) ([d6623d7](https://github.com/jamesholland-uk/pan-os-ansible/commit/d6623d78a365e6bb86a5f332a76fc96335528251)), closes [#139](https://github.com/jamesholland-uk/pan-os-ansible/issues/139)
* **panos_match_rule:** Always return rule result ([#171](https://github.com/jamesholland-uk/pan-os-ansible/issues/171)) ([2ae02ba](https://github.com/jamesholland-uk/pan-os-ansible/commit/2ae02ba6f17ae2ce0b8ad60524194bbc09968ad5)), closes [#170](https://github.com/jamesholland-uk/pan-os-ansible/issues/170)
* **panos_software:** Fix xpath invalid predicate on Python 3.6 ([#157](https://github.com/jamesholland-uk/pan-os-ansible/issues/157)) ([9e2e6af](https://github.com/jamesholland-uk/pan-os-ansible/commit/9e2e6af925537d47a74f97d5c549f335c7602feb)), closes [#155](https://github.com/jamesholland-uk/pan-os-ansible/issues/155)
* Don't look up color when state is absent ([#112](https://github.com/jamesholland-uk/pan-os-ansible/issues/112)) ([e55e7c0](https://github.com/jamesholland-uk/pan-os-ansible/commit/e55e7c018fe973341109470e3e545a679892f5ba)), closes [#26](https://github.com/jamesholland-uk/pan-os-ansible/issues/26)
* Handle if 'commit' isn't in params ([36247d4](https://github.com/jamesholland-uk/pan-os-ansible/commit/36247d4d44cdfbca4e00aae048b841f736424a8a))
* IPs not registering/unregistering correctly ([8405529](https://github.com/jamesholland-uk/pan-os-ansible/commit/8405529403fd1f378b055d558388d0dd8c46ce23))
* Mark commit option as deprecated ([#120](https://github.com/jamesholland-uk/pan-os-ansible/issues/120)) ([a20c752](https://github.com/jamesholland-uk/pan-os-ansible/commit/a20c752f04572ddfafe219148f90ea7c470ce95f)), closes [#115](https://github.com/jamesholland-uk/pan-os-ansible/issues/115)
* Remove 'operation' ([c9f653c](https://github.com/jamesholland-uk/pan-os-ansible/commit/c9f653ccea5aeaa13c3e8a83b61a16fd34c16dda))
* Rename error_on_shared to error_on_firewall_shared ([#137](https://github.com/jamesholland-uk/pan-os-ansible/issues/137)) ([2ab5b0a](https://github.com/jamesholland-uk/pan-os-ansible/commit/2ab5b0a85956f9e409c172ad640c9b10f787e4b4))
* Require 'local_ip_address', 'local_ip_address_type' together ([#99](https://github.com/jamesholland-uk/pan-os-ansible/issues/99)) ([87e6872](https://github.com/jamesholland-uk/pan-os-ansible/commit/87e68727476d027514fc492cbb645261b840d0c6)), closes [#83](https://github.com/jamesholland-uk/pan-os-ansible/issues/83)
* Require 'static_value' or 'dynamic_value' ([136d51c](https://github.com/jamesholland-uk/pan-os-ansible/commit/136d51c13f921c1784c4c86b67a4e5646c2de84c))
* Require Ansible 2.9.10 or greater ([#133](https://github.com/jamesholland-uk/pan-os-ansible/issues/133)) ([#134](https://github.com/jamesholland-uk/pan-os-ansible/issues/134)) ([ba3e08e](https://github.com/jamesholland-uk/pan-os-ansible/commit/ba3e08e7fa09ab2c38cc5426428cea9647c4a6ca))
* Results module warning ([#108](https://github.com/jamesholland-uk/pan-os-ansible/issues/108)) ([fe5c96e](https://github.com/jamesholland-uk/pan-os-ansible/commit/fe5c96e027e6e705e9bb402db406ba8e8f957afd)), closes [#106](https://github.com/jamesholland-uk/pan-os-ansible/issues/106)
* Support 'shared' for panos_security_rule_facts ([#126](https://github.com/jamesholland-uk/pan-os-ansible/issues/126)) ([da2cd61](https://github.com/jamesholland-uk/pan-os-ansible/commit/da2cd6152dd8e5611ecbd0418bce7b16cf23461d)), closes [#91](https://github.com/jamesholland-uk/pan-os-ansible/issues/91)
* **panos_administrator:** Add template_is_optional flag ([#76](https://github.com/jamesholland-uk/pan-os-ansible/issues/76)) ([158d3a0](https://github.com/jamesholland-uk/pan-os-ansible/commit/158d3a032523597c9b24895f478dc679fc211b2d)), closes [#43](https://github.com/jamesholland-uk/pan-os-ansible/issues/43)
* **requirements.txt:** Update requirements.txt ([#334](https://github.com/jamesholland-uk/pan-os-ansible/issues/334)) ([39f0be6](https://github.com/jamesholland-uk/pan-os-ansible/commit/39f0be6ab163031e33113995f8179eb77fb40a4a)), closes [#307](https://github.com/jamesholland-uk/pan-os-ansible/issues/307)
* Wrong else if ([#78](https://github.com/jamesholland-uk/pan-os-ansible/issues/78)) ([c35e38d](https://github.com/jamesholland-uk/pan-os-ansible/commit/c35e38d72aabe498f68a73e48146314d97704d9e))


### Performance Improvements

* **panos_address_object:** Enhanced performance ([ef3df93](https://github.com/jamesholland-uk/pan-os-ansible/commit/ef3df931b580228dee1adc667f36a8e7ac89957f))
* **plugins.module_utils.panos:** Add targetted refresh for the `listing` ([da7ff71](https://github.com/jamesholland-uk/pan-os-ansible/commit/da7ff71dfce41b234065af1d5cab1a330ca3ef81))


### Reverts

* "ci: updated 2.10 with new commit modules" ([89e34be](https://github.com/jamesholland-uk/pan-os-ansible/commit/89e34beb0b935adcf39d398a97ec594e8af6e7e1))
* "Updated with new commit modules" ([3d53dec](https://github.com/jamesholland-uk/pan-os-ansible/commit/3d53deca4403d1bf1b1cbffba3946db93620d660))
* Revert "ci: Temporarily build docs" ([4a1bac0](https://github.com/jamesholland-uk/pan-os-ansible/commit/4a1bac047188371cf0e47148111bdbeddce0e82c))

### [2.17.7](https://github.com/PaloAltoNetworks/pan-os-ansible/compare/v2.17.6...v2.17.7) (2023-10-05)


### Bug Fixes

* **various:** Remove unused imports for pylint testing ([#495](https://github.com/PaloAltoNetworks/pan-os-ansible/issues/495)) ([71aecd6](https://github.com/PaloAltoNetworks/pan-os-ansible/commit/71aecd6ec2128c8035e1ad40479e9c059fa27388))

### [2.17.6](https://github.com/PaloAltoNetworks/pan-os-ansible/compare/v2.17.5...v2.17.6) (2023-09-14)


### Bug Fixes

* **gathered_filter:** Fix error handling for no-value operators ([#489](https://github.com/PaloAltoNetworks/pan-os-ansible/issues/489)) ([351960c](https://github.com/PaloAltoNetworks/pan-os-ansible/commit/351960c90624b299ce8cdd35146d95bd941ed22c))

### [2.17.5](https://github.com/PaloAltoNetworks/pan-os-ansible/compare/v2.17.4...v2.17.5) (2023-09-08)


### Bug Fixes

* **gathered_filter:** Update logic to cover cases of None ([#488](https://github.com/PaloAltoNetworks/pan-os-ansible/issues/488)) ([d2372c5](https://github.com/PaloAltoNetworks/pan-os-ansible/commit/d2372c5f9e3a26f047859e3feed5ab647970c631))
* **panos_device_group:** Do not move a Device Group if state is set to gathered ([#484](https://github.com/PaloAltoNetworks/pan-os-ansible/issues/484)) ([93d61a7](https://github.com/PaloAltoNetworks/pan-os-ansible/commit/93d61a76cb81342c4ef743b7bce28e6132120288))

### [2.17.4](https://github.com/PaloAltoNetworks/pan-os-ansible/compare/v2.17.3...v2.17.4) (2023-08-15)


### Bug Fixes

* **event-driven ansible:** Update for Red Hat's certification checks ([#479](https://github.com/PaloAltoNetworks/pan-os-ansible/issues/479)) ([0fdce26](https://github.com/PaloAltoNetworks/pan-os-ansible/commit/0fdce2660dd357b5a5e3cde706068f89655c6a4f))

### [2.17.3](https://github.com/PaloAltoNetworks/pan-os-ansible/compare/v2.17.2...v2.17.3) (2023-07-11)


### Bug Fixes

* **eda:** Make `custom_logger` argument optional ([#456](https://github.com/PaloAltoNetworks/pan-os-ansible/issues/456)) ([49ed307](https://github.com/PaloAltoNetworks/pan-os-ansible/commit/49ed3079e646072401075b68da07bd0799818e42))
* **panos_admpwd:** Fix success criteria and update example in docs ([#457](https://github.com/PaloAltoNetworks/pan-os-ansible/issues/457)) ([9ecdb65](https://github.com/PaloAltoNetworks/pan-os-ansible/commit/9ecdb65bb88db4528cbae7221f4ea930a62e49c9))
* **panos_bgp_peer_group:** Fix for IBGP export next-hop options ([#459](https://github.com/PaloAltoNetworks/pan-os-ansible/issues/459)) ([9489fa2](https://github.com/PaloAltoNetworks/pan-os-ansible/commit/9489fa25b6f3f898aa6c080d6f1676c1747e073f))
* **panos_ike_crypto_profile:** Update DH group choices ([#461](https://github.com/PaloAltoNetworks/pan-os-ansible/issues/461)) ([8194318](https://github.com/PaloAltoNetworks/pan-os-ansible/commit/8194318c496f192e9eb63526cc7a13df4f1ca493))
* **panos_ipsec_profile:** Update DH group choices ([#462](https://github.com/PaloAltoNetworks/pan-os-ansible/issues/462)) ([1798a3b](https://github.com/PaloAltoNetworks/pan-os-ansible/commit/1798a3b0ab7b4cf415d44df0c13d96cec5111252))
* **panos_software:** Modify valid sequence for downloads only ([#463](https://github.com/PaloAltoNetworks/pan-os-ansible/issues/463)) ([214c4bb](https://github.com/PaloAltoNetworks/pan-os-ansible/commit/214c4bb9f2c7a9421694f808ba8f0f83e635dca5))

### [2.17.2](https://github.com/PaloAltoNetworks/pan-os-ansible/compare/v2.17.1...v2.17.2) (2023-06-28)


### Bug Fixes

* **panos_ike_crypto_profile:** Fixed auth type `non-auth` for IKE profile ([#418](https://github.com/PaloAltoNetworks/pan-os-ansible/issues/418)) ([0a2abe8](https://github.com/PaloAltoNetworks/pan-os-ansible/commit/0a2abe80055982ddf2035d24f9adde36ce226a55))

### [2.17.1](https://github.com/PaloAltoNetworks/pan-os-ansible/compare/v2.17.0...v2.17.1) (2023-06-23)


### Bug Fixes

* Tox-compliant EDA code, and Tox checks in CI ([#453](https://github.com/PaloAltoNetworks/pan-os-ansible/issues/453)) ([9a50c9b](https://github.com/PaloAltoNetworks/pan-os-ansible/commit/9a50c9bb5e841ddfe0eeca7ea9021eb289e0e5db))
* **eda:** Move EDA plugin to correct path ([#444](https://github.com/PaloAltoNetworks/pan-os-ansible/issues/444)) ([dc524e9](https://github.com/PaloAltoNetworks/pan-os-ansible/commit/dc524e93b87f0163cc3019636617198a59ebf51f))

## [2.17.0](https://github.com/PaloAltoNetworks/pan-os-ansible/compare/v2.16.0...v2.17.0) (2023-06-14)


### Features

* **panos_export:** Create directory if it doesn't exist ([#434](https://github.com/PaloAltoNetworks/pan-os-ansible/issues/434)) ([9422af0](https://github.com/PaloAltoNetworks/pan-os-ansible/commit/9422af0b17d1d534c73391cc95640ad6dea3d824))
* **panos_import:** Add private key blocking to keypair import ([#417](https://github.com/PaloAltoNetworks/pan-os-ansible/issues/417)) ([3fd5bac](https://github.com/PaloAltoNetworks/pan-os-ansible/commit/3fd5bacdd0324ab636a0456f19993d588f900dcb))
* **panos_software:** name config load option ([#398](https://github.com/PaloAltoNetworks/pan-os-ansible/issues/398)) ([378d5a6](https://github.com/PaloAltoNetworks/pan-os-ansible/commit/378d5a679463918dd2e635f20ba0b086f50feb97))

## [2.16.0](https://github.com/PaloAltoNetworks/pan-os-ansible/compare/v2.15.0...v2.16.0) (2023-05-12)


### Features

* **event_driven_ansible:** New plugin for event-driven ansible ([c4b627d](https://github.com/PaloAltoNetworks/pan-os-ansible/commit/c4b627dac496f7233ca6016aa85f60c8378ada41))
* **panos_log_forwarding_profile_match_list:** Add decryption log-type to log forwarding ([#429](https://github.com/PaloAltoNetworks/pan-os-ansible/issues/429)) ([a1dab0a](https://github.com/PaloAltoNetworks/pan-os-ansible/commit/a1dab0a2b14f3ba1fa566161ce1a3f28819683cb))

## [2.15.0](https://github.com/PaloAltoNetworks/pan-os-ansible/compare/v2.14.0...v2.15.0) (2023-04-27)


### Features

* **panos_http_profile:** Decrypt and GP for HTTP profiles ([#427](https://github.com/PaloAltoNetworks/pan-os-ansible/issues/427)) ([f6c86d9](https://github.com/PaloAltoNetworks/pan-os-ansible/commit/f6c86d9d592ea7e4b17d7e4186ffb18c2349e359))

## [2.14.0](https://github.com/PaloAltoNetworks/pan-os-ansible/compare/v2.13.3...v2.14.0) (2023-04-26)


### Features

* **panos_aggregate_interface:** Fast failover for LACP on aggregate network interfaces ([#423](https://github.com/PaloAltoNetworks/pan-os-ansible/issues/423)) ([ad89bcd](https://github.com/PaloAltoNetworks/pan-os-ansible/commit/ad89bcd46ec46b5b1cb6d6363f8f13db0ba5655f))

# Changelog

Details can be found [here](https://github.com/PaloAltoNetworks/pan-os-ansible/releases)
