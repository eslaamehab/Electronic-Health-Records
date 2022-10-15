// SPDX-License-Identifier: GPL-3.0
pragma experimental ABIEncoderV2;
pragma solidity >=0.6.0 <0.9.0;

/*
 * @title Storage
 * @dev Store & retrieve value in a variable
 * @custom:dev-run-script ./scripts/deploy_with_ethers.ts
 */
contract SimpleStorage {
    uint256 patient_id;
    uint256 doctor_id;
    string name;
    string height;
    string sex;
    string weight;
    string age;
    string readings;
    bytes previousBlockAddress;

    constructor(
        uint256 patientId,
        uint256 doctorId,
        string memory names,
        string memory ages,
        string memory sexs,
        string memory heights,
        string memory weights,
        string memory readingss,
        bytes memory blockAddresss
    ) public {
        patient_id = patientId;
        doctor_id = doctorId;
        name = names;
        age = ages;
        sex = sexs;
        height = heights;
        weight = weights;
        readings = readingss;
        previousBlockAddress = blockAddresss;
    }

    function retrieve()
        public
        view
        returns (
            uint256,
            uint256,
            string memory,
            string memory,
            string memory,
            string memory,
            string memory,
            string memory,
            bytes memory
        )
    {
        return (
            patient_id,
            doctor_id,
            name,
            age,
            sex,
            height,
            weight,
            readings,
            previousBlockAddress
        );
    }
    // uint256 public number;

    // struct patient {
    //     uint256 id;
    //     string name;
    //     string sex;
    //     uint256 age;
    //     uint256 weight;
    //     uint256 height;
    //     string readings;
    // }

    // struct visit {
    //     uint256 patientid;
    //     uint256 doctorid;
    //     string readings;
    //     string reason;
    //     string notes;
    //     string labtests;
    // }

    // struct doctor {
    //     uint256 id;
    //     string name;
    //     string privatekey;
    // }

    // mapping(address => patient) PatientMap;
    // mapping(address => visit) VistMap;
    // address[] public patients;
    // address[] public visits;

    // function _storepatient(
    //     uint256 id,
    //     address _address,
    //     string memory _name,
    //     string memory _sex,
    //     uint256 age,
    //     uint256 weight,
    //     uint256 height,
    //     string memory _readings
    // ) public {
    //     //creating the object of the structure in solidity
    //     patient storage patientt = PatientMap[_address];

    //     patientt.id = id;
    //     patientt.name = _name;
    //     patientt.sex = _sex;
    //     patientt.age = age;
    //     patientt.weight = weight;
    //     patientt.height = height;
    //     patientt.readings = _readings;

    //     patients.push(_address);

    //     // patients.push(
    //     //     patient(
    //     //         //uint256(keccak256(abi.encodePacked(_name))),
    //     //         id,
    //     //         _name,
    //     //         _sex,
    //     //         age,
    //     //         weight,
    //     //         height,
    //     //         _readings
    //     //     )
    //     // );
    // }

    // function _addvisit(
    //     address _address,
    //     uint256 patientid,
    //     uint256 doctorid,
    //     string memory _readings,
    //     string memory _reason,
    //     string memory _notes,
    //     string memory _labtests
    // ) public {
    //     visit storage visitt = VistMap[_address];

    //     visitt.patientid = patientid;
    //     visitt.doctorid = doctorid;
    //     visitt.readings = _readings;
    //     visitt.reason = _reason;
    //     visitt.notes = _notes;
    //     visitt.labtests = _labtests;

    //     visits.push(_address);
    // }

    // function _retrievepatientAddress() public view returns (address[] memory) {
    //     return patients;
    // }

    // function getpatient(address _address)
    //     public
    //     view
    //     returns (
    //         uint256,
    //         uint256,
    //         string memory,
    //         string memory,
    //         uint256,
    //         uint256,
    //         string memory
    //     )
    // {
    //     return (
    //         PatientMap[_address].id,
    //         PatientMap[_address].age,
    //         PatientMap[_address].name,
    //         PatientMap[_address].sex,
    //         PatientMap[_address].weight,
    //         PatientMap[_address].height,
    //         PatientMap[_address].readings
    //     );
    // }

    // function getvisit(address _address)
    //     public
    //     view
    //     returns (
    //         uint256,
    //         uint256,
    //         string memory,
    //         string memory,
    //         string memory,
    //         string memory
    //     )
    // {
    //     return (
    //         VistMap[_address].patientid,
    //         VistMap[_address].doctorid,
    //         VistMap[_address].readings,
    //         VistMap[_address].reason,
    //         VistMap[_address].notes,
    //         VistMap[_address].labtests
    //     );
    // }

    /*
     * @dev Store value in variable
     * @param num value to store
     */
    // function store(uint256 num) public {
    //     number = num;
    //     // uint256 test =4;
    // }

    // /*
    //  * @dev Return value
    //  * @return value of 'number'
    //  */

    // function retrieve() public view returns (uint256) {
    //     return number;
    // }
}
