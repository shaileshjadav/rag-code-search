import { Anchor, Avatar, Menu } from "@mantine/core";
import { IconBrandGithub, IconReportAnalytics } from "@tabler/icons-react";
import classes from "./Avatar.module.css"

type AvatarProps = {
    githubUserName:string,
    profileLetters:string,
}
export function UserAvatar(props: AvatarProps) {
  return (
    <Menu shadow="md" width={200}>
      <Menu.Target>
        <Avatar color="dark" radius="xl">{props.profileLetters}</Avatar>
      </Menu.Target>

      <Menu.Dropdown>
        <Menu.Label>{props.githubUserName}</Menu.Label>
        <Menu.Item leftSection={<IconBrandGithub size={20} />}>
          <Anchor href={`https://github.com/${props.githubUserName}`} target="_blank" underline="never" size="md" className={classes.link}>
            Profile
          </Anchor>
        </Menu.Item>
        <Menu.Item leftSection={<IconReportAnalytics size={20} />}>
          <Anchor href={`https://github.com/${props.githubUserName}?tab=repositories`} target="_blank" underline="never" size="md" className={classes.link}>
            Repositories
          </Anchor>
        </Menu.Item>
      </Menu.Dropdown>
    </Menu>
  );
}
