// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
contract DonationContract {

    mapping(address => uint256) public senderAddress;
    mapping(uint256 => Donation) public allDonations;
    uint256 public donationCount;

    event DonationMade(address indexed donor, uint256 amount, uint256 timestamp);

    struct Donation {
        address donor;
        uint256 amount;
        uint256 timestamp;
    }

    function donate() public payable {
        require(msg.value > 0, "Donation amount must be greater than zero");

        Donation memory newDonation = Donation({
            donor: msg.sender,
            amount: msg.value,
            timestamp: block.timestamp
        });

        donationCount++;
        allDonations[donationCount] = newDonation;
        senderAddress[msg.sender] += msg.value;
        emit DonationMade(msg.sender, msg.value, block.timestamp);
    }

    function getAllDonations() public view returns (Donation[] memory) {
        Donation[] memory donations = new Donation[](donationCount);
        for (uint256 i = 1; i <= donationCount; i++) {
            donations[i - 1] = allDonations[i];
        }
        return donations;
    }
}