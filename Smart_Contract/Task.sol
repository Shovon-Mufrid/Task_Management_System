// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TaskManagement {
    // Define the Task Struct
    struct Task {
        uint256 id;
        string name;
        string description;
        uint256 assignedTime;
        uint256 deadline;
        string status;
    }

    // Contract
    Task[] tasks;
    mapping(uint256 => address) public taskToOwner;
    mapping(uint256 => uint256) public taskToIndex;

    // Create
    function createTask(
        uint256 _id,
        string memory _name,
        string memory _description,
        uint256 _assignedTime,
        uint256 _deadline,
        string memory _status
    ) public {
        Task memory newTask = Task({
            id: _id,
            name: _name,
            description: _description,
            assignedTime: _assignedTime,
            deadline: _deadline,
            status: _status
        });
        tasks.push(newTask);
        uint256 taskId = tasks.length - 1;
        taskToOwner[taskId] = msg.sender;
        taskToIndex[_id] = taskId;
    }

    // Update
    function editTask(
        uint256 _id,
        string memory _name,
        string memory _description,
        uint256 _assignedTime,
        uint256 _deadline,
        string memory _status
    ) public {
        uint256 taskId = taskToIndex[_id];
        require(taskToOwner[taskId] == msg.sender, "You are not the owner of this task");
        Task storage taskToUpdate = tasks[taskId];
        taskToUpdate.name = _name;
        taskToUpdate.description = _description;
        taskToUpdate.assignedTime = _assignedTime;
        taskToUpdate.deadline = _deadline;
        taskToUpdate.status = _status;
    }

    // Read
    function readTask(uint256 _id) public view returns (Task memory) {
        uint256 taskId = taskToIndex[_id];
        return tasks[taskId];
    }

    // Delete
    function deleteTask(uint256 _id) public {
        uint256 taskId = taskToIndex[_id];
        require(taskToOwner[taskId] == msg.sender, "You are not the owner of this task");
        delete tasks[taskId];
        delete taskToOwner[taskId];
        delete taskToIndex[_id];
    }

    // GET Status
    function getTaskStatus(uint256 _id) public view returns (string memory) {
        uint256 taskId = taskToIndex[_id];
        return tasks[taskId].status;
    }

    // GET Name 
    function getTaskName(uint256 _id) public view returns (string memory) {
        uint256 taskId = taskToIndex[_id];
        return tasks[taskId].name;
    }

    // GET Assigned Time 
    function getTaskAssignedTime(uint256 _id) public view returns (uint256) {
        uint256 taskId = taskToIndex[_id];
        return tasks[taskId].assignedTime;
    }

    // GET Deadline
    function getTaskDeadline(uint256 _id) public view returns (uint256) {
        uint256 taskId = taskToIndex[_id];
        return tasks[taskId].deadline;
    }

}