### [2.19.1](https://github.com/PaloAltoNetworks/pan-os-ansible/compare/v2.19.0...v2.19.1) (2023-12-14)


### Bug Fixes

* define in pyproject.toml Python 3.9 for ansible-core 2.14 ([#522](https://github.com/PaloAltoNetworks/pan-os-ansible/issues/522)) ([d4cd846](https://github.com/PaloAltoNetworks/pan-os-ansible/commit/d4cd84640502eee7822688167f6dc93412e19b0a))

## [2.19.0](https://github.com/PaloAltoNetworks/pan-os-ansible/compare/v2.18.0...v2.19.0) (2023-12-13)


### Features

* **module/panos_edl:** New module for External Dynamic Lists ([#512](https://github.com/PaloAltoNetworks/pan-os-ansible/issues/512)) ([1e33995](https://github.com/PaloAltoNetworks/pan-os-ansible/commit/1e3399536101c3ab426158724fe2948e7ffde50e))

## [2.18.0](https://github.com/PaloAltoNetworks/pan-os-ansible/compare/v2.17.8...v2.18.0) (2023-11-29)


### Features

* **upgrade_assurance:** add upgrade assurance modules ([40b0d0d](https://github.com/PaloAltoNetworks/pan-os-ansible/commit/40b0d0dc442c1c62231e63c95479a0b212df5ad6))


### Bug Fixes

* **upgrade_assurance:** error out panorama connections ([218e2d2](https://github.com/PaloAltoNetworks/pan-os-ansible/commit/218e2d2a1b53cd04e48b4f92de48feb23a5e9f0e))

### [2.17.8](https://github.com/PaloAltoNetworks/pan-os-ansible/compare/v2.17.7...v2.17.8) (2023-10-23)


### Bug Fixes

* **panos_export:** Fix create_directory for panos_export for binary files ([#492](https://github.com/PaloAltoNetworks/pan-os-ansible/issues/492)) ([d0f8572](https://github.com/PaloAltoNetworks/pan-os-ansible/commit/d0f8572eabf1419ccd004a3ec8cb628409fea7ff))

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
