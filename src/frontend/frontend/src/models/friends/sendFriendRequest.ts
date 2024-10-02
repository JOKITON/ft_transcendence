import FriendRequest from './friendRequest';

export interface sendFriendRequest{
    fromUser: string,
    toUser: string,
    existingRequests?: FriendRequest[]
}