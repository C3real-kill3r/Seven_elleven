null = None

create_profile_query = """
mutation{
  createProfile(bio:"hello people", birthDate:"2018-12-19", image:"leo.jp",location:"Nairobi", userId:1){
    profile{id,user{username},bio}
  }
}
"""

get_profiles_query = """
query{
  allProfiles{
    id
    user{username}
    image
    bio
    location
    birthDate
  }
}
"""
